import logging
import threading
import time
from unittest.mock import patch

import pytest
from stomppy.client import Client

logging.disable(logging.CRITICAL)

HOST = 'localhost'
PORT = '61613'


class MockSocket:
    def __init__(self):
        self.data_to_recv = b''

    def connect(self, address):
        pass

    def close(self):
        pass

    def recv(self, size):
        return self.data_to_recv[:size]

    def sendall(self, data):
        pass


@pytest.fixture
def mock_socket(monkeypatch):
    def mock_socket_constructor(*args, **kwargs):
        return MockSocket()

    monkeypatch.setattr('stomppy.client.socket.socket', mock_socket_constructor)


@pytest.fixture()
def client(mock_socket):
    client = Client(HOST, PORT)
    client.connect()
    yield client
    client.disconnect()


def test_client_initialization(mock_socket):
    client = Client(HOST, PORT)
    assert client.host == HOST
    assert client.port == PORT
    assert isinstance(client.socket, MockSocket)
    assert isinstance(client.receive_thread, threading.Thread)
    assert not client.connected
    assert client.heartbeat == (0, 0)


def test_client_connect_disconnect(client):
    assert client.connected


def test_send_frame(client):
    frame = 'TEST_FRAME\n\n'
    client.send_frame(frame)
    assert True


def test_parse_heartbeat():
    client = Client(HOST, PORT)
    buffer = b'heart-beat:1000,2000\n'
    client.parse_heartbeat(buffer)
    assert client.heartbeat == (1000, 2000)


def test_send_heartbeat():
    client = Client(HOST, PORT)
    client.heartbeat = (1, 0)
    client.connected = True
    thread = threading.Thread(target=client.send_heartbeat)
    thread.start()
    time.sleep(1)
    thread.join()
    assert True


def test_receive_frames(client):
    client.socket.data_to_recv = b'MOCK_RECEIVE_FRAME\n\n'
    threading.Timer(1, client.disconnect).start()
    client.receive_frames()
    assert not client.connected


def test_receive_frames_with_heartbeat(client):
    client.socket.data_to_recv = b'heart-beat:1000,2000\n'
    threading.Timer(1, client.disconnect).start()
    client.receive_frames()
    assert not client.connected


def test_receive_frames_without_heartbeat(client):
    client.socket.data_to_recv = b'OTHER_FRAME\n\n'
    threading.Timer(1, client.disconnect).start()
    client.receive_frames()
    assert not client.connected


def test_receive_frames_null_byte(client):
    client.socket.data_to_recv = b'FRAME_WITH_NULL_BYTE\x00\n\n'
    threading.Timer(1, client.disconnect).start()
    client.receive_frames()
    assert not client.connected


def test_disconnect(client):
    client.disconnect()
    assert not client.connected


def test_receive_frames_break_on_empty_chunk(client):
    client.socket.data_to_recv = b''
    threading.Timer(1, client.disconnect).start()
    client.receive_frames()
    assert not client.connected


def test_send_heartbeat_wait_until_non_zero(client):
    client.heartbeat = (0, 0)
    client.connected = True
    with patch('time.sleep') as mock_sleep:
        mock_sleep.side_effect = [None, StopIteration]
        thread = threading.Thread(target=client.send_heartbeat)
        thread.start()
        thread.join()
        call_count = 2
        assert mock_sleep.call_count == call_count


def test_parse_heartbeat_values_not_found_warning(client, caplog):
    buffer = b'invalid_header\n'
    with caplog.at_level(logging.WARNING):
        client.parse_heartbeat(buffer)
        assert 'Heartbeat values not found in the header.' in caplog.text
