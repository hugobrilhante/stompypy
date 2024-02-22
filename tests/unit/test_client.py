from unittest.mock import Mock
from unittest.mock import patch

import pytest

from src.stompypy.client import Client
from src.stompypy.exceptions import ClientError

HOST = 'localhost'
PORT = 1234
TEST_FRAME = 'test_frame'
HEARTBEAT_VALUES = (10000, 10000)
CONNECT_STRING = 'socket.socket.connect'


@pytest.fixture
def client():
    client = Client(HOST, PORT)
    yield client
    client.disconnect()


def test_connect(client):
    with patch(CONNECT_STRING) as mock_connect:
        client.connect()
        mock_connect.assert_called_once_with((HOST, PORT))


def test_disconnect(client):
    with patch('socket.socket.close') as mock_close:
        client.disconnect()
        mock_close.assert_called_once()


def test_send_frame(client):
    with patch(CONNECT_STRING):
        with patch('socket.socket.sendall') as mock_sendall:
            client.send_frame(TEST_FRAME)
            mock_sendall.assert_called_once_with(TEST_FRAME.encode())


def test_add_listener(client):
    listener = Mock()
    client.add_listener(listener)
    assert listener in client.event_manager.listeners


def test_receive_frames(client):
    with patch(CONNECT_STRING):
        with patch('socket.socket.recv', side_effect=[b'test_frame\n', b'\n']) as mock_recv:
            with pytest.raises(ClientError):
                client.connected.set()
                client.receive_frames()
            call_count = 3
            assert mock_recv.call_count == call_count


def test_parse_heartbeat(client):
    headers = {'heart-beat': f'{HEARTBEAT_VALUES[0]},{HEARTBEAT_VALUES[1]}'}
    client._parse_heartbeat(headers)
    assert client.heartbeat == HEARTBEAT_VALUES


def test_start_receive_thread(client):
    with patch('threading.Thread.start') as mock_start:
        client._start_receive_thread()
        mock_start.assert_called_once()


def test_start_heartbeat_thread(client):
    with patch('threading.Thread.start') as mock_start:
        client.heartbeat = (1, 1)
        client._start_heartbeat_thread()
        mock_start.assert_called_once()


def test_exit(client):
    with pytest.raises(ClientError):
        with Client(HOST, PORT):
            raise ClientError('Test exception')
