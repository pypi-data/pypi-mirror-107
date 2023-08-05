# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import base64
import functools
import hashlib
import json
import logging
import os
import os.path
import platform
import threading
import typing

import websockets

logger = logging.getLogger(__name__)


# We need to use this syntax of creating TypeDict because “from” is a reserved keyword in Python.
TransferTx = typing.TypedDict(
    'TransferTx',
    {
        'type': int,
        'from': bytes,
        'to': bytes,
        'value': int,
        'message': bytes,
        'hash': str,
        'height': int,
        'fee': int,
        'raw': bytes,
        'index': int,
    },
)


def _b64_to_bytes(b64: str) -> bytes:
    return base64.decodebytes(b64.encode('ascii'))


def _b64_to_str(b64: str) -> str:
    return _b64_to_bytes(b64).decode('ascii')


def _iter_event_attrs(attrs) -> typing.Iterator[typing.Tuple[str, typing.Optional[str]]]:
    for attr in attrs:
        key = _b64_to_str(attr['key'])
        value = None if (maybe_value_b64 := attr['value']) is None else _b64_to_str(maybe_value_b64)
        yield key, value


def _events_to_dict(events):
    d = {}
    for event in events:
        assert event['type'] == 'tx'
        for key, value in _iter_event_attrs(event['attributes']):
            if key in {'type', 'value', 'height', 'fee', 'index'}:
                value_prime = int(value)
            elif key in {'from', 'to', 'message'}:
                value_prime = _b64_to_bytes(value or '')
            else:
                value_prime = value
            d[key] = value_prime
    return d


def _subscription_msg_to_tx(tx_msg) -> TransferTx:
    tx_result = tx_msg['result']['data']['value']['TxResult']
    tx = _events_to_dict(tx_result['result']['events'])
    tx['raw'] = base64.decodebytes(tx_result['tx'].encode('ascii'))
    tx['index'] = tx_result['index']
    tx['height'] = int(tx_result['height'])
    for key, value in tx_msg['result']['events'].items():
        if key == 'tx.hash':
            tx['hash'] = value[0]
            break
    return TransferTx(**tx)


def _search_result_to_tx(search_result) -> TransferTx:
    tx = _events_to_dict(search_result['tx_result']['events'])
    tx['raw'] = _b64_to_bytes(search_result['tx'])
    tx['index'] = search_result['index']
    tx['hash'] = search_result['hash']
    tx['height'] = int(search_result['height'])
    return TransferTx(**tx)


def get_local_data_dir():
    system = platform.system()
    if system == 'Windows':
        return os.environ['LocalAppData']
    elif system == 'Darwin':
        return os.path.join(
            os.environ['HOME'],
            'Library',
            'Application Support',
        )
    else:
        return os.getenv(
            'XDG_DATA_HOME',
            os.path.join(os.environ['HOME'], '.local', 'share'),
        )


JSONRequestID = int


class TendermintServerError(Exception):
    pass


class JSONRPCClient:
    def __init__(self, ws):
        self._ws = ws
        self._counter = 0
        self._counter_lock = threading.Lock()

    def _get_new_id(self):
        self._counter_lock.acquire()
        self._counter += 1
        try:
            return self._counter
        finally:
            self._counter_lock.release()

    async def req(self, method, params) -> JSONRequestID:
        id_ = self._get_new_id()
        body = json.dumps(
            {
                'jsonrpc': '2.0',
                'id': id_,
                'method': method,
                'params': params,
            })
        await self._ws.send(body)
        return id_

    async def recv(self) -> dict:
        msg = json.loads(await self._ws.recv())
        if msg.get('error'):
            error_desc = msg["error"]["data"]
            logger.error(f'Received server error: “{error_desc}”')
            raise TendermintServerError(error_desc)
        return msg


Height = typing.NewType('Height', int)
TxHash = typing.NewType('TxHash', str)
Base64String = typing.NewType('Base64String', str)
Address = typing.NewType('Address', typing.Union[Base64String, bytes])


def _maybe_enforce_b64(maybe_address: typing.Optional[Address]) -> typing.Optional[Base64String]:
    if isinstance(maybe_address, str):
        return maybe_address
    elif isinstance(maybe_address, bytes):
        return base64.encodebytes(maybe_address).decode("ascii").strip()


class ErcoinReactor:
    retry_timeout = 10

    def __init__(
            self,
            *,
            node,
            to_address: typing.Optional[Address] = None,
            from_address: typing.Optional[Address] = None,
            ssl=True,
            port=26657,
    ):
        """Initialize reactor.

        to_address and from_address cannot be given simultaneously.
        """

        if to_address and from_address:
            raise ValueError('At most one address can be given.')

        self._node = node
        self._to_address_b64 = _maybe_enforce_b64(to_address)
        self._from_address_b64 = _maybe_enforce_b64(from_address)
        self._port = port
        self._ssl = ssl

        self._tx_buf: typing.List[TransferTx] = []
        self._seen_tx_hashes: typing.Set[str] = set()
        self._catched_up = False

    def _endpoint(self):
        protocol = 'wss' if self._ssl else 'ws'
        return f'{protocol}://{self._node}:{self._port}/websocket'

    @functools.cached_property
    def _subscription_query(self):
        return self._join_queries([
            "tm.event='Tx'",
            self._base_tx_query,
        ])

    @functools.cached_property
    def _catchup_query(self):
        return self._join_queries([
            self._base_tx_query,
            f'tx.height >= {self._last_height}',
        ])

    @functools.cached_property
    def _base_tx_query(self):
        if self._to_address_b64:
            return f"tx.to='{self._to_address_b64}'"
        elif self._from_address_b64:
            return f"tx.from='{self._from_address_b64}'"
        return ''

    @staticmethod
    def _join_queries(queries):
        return ' AND '.join(query for query in queries if query)

    @functools.cached_property
    def _state_filepath(self):
        h = hashlib.new('sha224')
        h.update(self._base_tx_query.encode('ascii'))
        basename = h.digest().hex()

        return os.path.join(
            get_local_data_dir(),
            'ern_reactor',
            self.get_namespace(),
            f'{basename}.json',
        )

    def _load_state(self) -> typing.Optional[dict]:
        state_filename = self._state_filepath
        if os.path.isfile(state_filename):
            with open(state_filename) as f:
                return json.load(f)

    def _dump_state(self, state):
        tmp_filepath = self._state_filepath + '.tmp'
        dirpath = os.path.dirname(self._state_filepath)
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        with open(tmp_filepath, 'w') as f:
            json.dump(state, f)
        os.replace(tmp_filepath, self._state_filepath)

    def _load_sync_status(self) -> None:
        if (state := self._load_state()) is None:
            self._last_height = 0
            self._last_index = 0
        else:
            self._last_height = state['height']
            self._last_index = state['index']

    def _save_sync_status(self) -> None:
        state = self._load_state() or {}
        state['height'] = self._last_height
        state['index'] = self._last_index
        self._dump_state(state)

    async def _start_catchup(self):
        self._last_catchup_page = 0
        return await self._continue_catchup()

    async def _continue_catchup(self) -> JSONRequestID:
        self._last_catchup_page += 1
        return await self._rpc_client.req(
            'tx_search',
            {
                'query': self._catchup_query,
                'page': str(self._last_catchup_page),
                'per_page': '100',
            },
        )

    async def _handle_connection(self, ws):
        self._rpc_client = JSONRPCClient(ws)
        subscribe_id = await self._rpc_client.req('subscribe', {'query': self._subscription_query})
        subscribe_resp = await self._rpc_client.recv()
        assert subscribe_resp.get('result') == {}
        catchup_id = await self._start_catchup()
        while True:
            msg = await self._rpc_client.recv()
            if (msg_id := msg['id']) == catchup_id:
                self._catched_up = int(msg['result']['total_count']) <= self._last_catchup_page * 100
                if not self._catched_up:
                    catchup_id = await self._continue_catchup()
                await self._handle_txs(_search_result_to_tx(res) for res in msg['result']['txs'])
                if self._catched_up:
                    await self._handle_txs(self._tx_buf)
            elif msg_id == subscribe_id:
                assert msg['result']['data']['type'] == 'tendermint/event/Tx'
                await self._handle_tx(_subscription_msg_to_tx(msg))

    async def start(self) -> typing.NoReturn:
        self._load_sync_status()
        while True:
            try:
                async with websockets.connect(self._endpoint()) as ws:
                    await self._handle_connection(ws)
            except (websockets.exceptions.ConnectionClosedError, ConnectionError, TendermintServerError):
                logger.warning(f'Connection error, sleeping {self.retry_timeout}s before retrying…')
                await asyncio.sleep(self.retry_timeout)

    async def _handle_tx(self, tx: TransferTx):
        index = tx['index']
        height = tx['height']
        if (height, index) <= (self._last_height, self._last_index):
            logger.debug(f'Omitting already processed transaction {tx["hash"]} at height {height} and index {index}.')
            return
        await self.process_tx(tx)
        self._last_height = tx['height']
        self._last_index = tx['index']
        self._save_sync_status()

    async def _handle_txs(self, txs):
        for tx in txs:
            await self._handle_tx(tx)

    def get_namespace(self) -> str:
        """Return namespace used to distinguish different instances of the reactor."""
        raise NotImplementedError()

    async def process_tx(self, tx: TransferTx) -> None:
        raise NotImplementedError()
