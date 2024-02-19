from unittest.mock import MagicMock

import pytest
from stomppy.sender import Sender


@pytest.fixture
def client():
    return MagicMock()


def test_send_frame(client):
    sender = Sender(client)
    sender.send_frame('test_frame')
    client.send_frame.assert_called_once_with('test_frame')


def test_ack(client):
    sender = Sender(client)
    sender.ack('message_id')
    client.send_frame.assert_called_once_with('ACK\nid:message_id\n\n\x00')


def test_abort(client):
    sender = Sender(client)
    sender.abort('tx1')
    client.send_frame.assert_called_once_with('ABORT\ntransaction:tx1\n\n\x00')


def test_begin(client):
    sender = Sender(client)
    sender.begin('tx1')
    client.send_frame.assert_called_once_with('BEGIN\ntransaction:tx1\n\n\x00')


def test_commit(client):
    sender = Sender(client)
    sender.commit('tx1')
    client.send_frame.assert_called_once_with('COMMIT\ntransaction:tx1\n\n\x00')


def test_connect(client):
    sender = Sender(client)
    sender.connect('localhost', '1.2', 'user', 'pass', '1000,1000')
    client.send_frame.assert_called_once_with(
        'CONNECT\nhost:localhost\naccept-version:1.2\nlogin:user\npasscode:pass\nheart-beat:1000,1000\n\n\x00'
    )


def test_disconnect(client):
    sender = Sender(client)
    sender.disconnect('receipt123')
    client.send_frame.assert_called_once_with('DISCONNECT\nreceipt:receipt123\n\n\x00')


def test_nack(client):
    sender = Sender(client)
    sender.nack('message_id')
    client.send_frame.assert_called_once_with('NACK\nid:message_id\n\n\x00')


def test_send(client):
    sender = Sender(client)
    sender.send('queue', 'text/plain', 'Hello', 'tx1')
    client.send_frame.assert_called_once_with(
        'SEND\ndestination:queue\ncontent-type:text/plain\ntransaction:tx1\n\nHello\n\n\x00'
    )


def test_subscribe(client):
    sender = Sender(client)
    sender.subscribe('sub1', 'queue', 'client-individual')
    client.send_frame.assert_called_once_with('SUBSCRIBE\nid:sub1\ndestination:queue\nack:client-individual\n\n\x00')


def test_unsubscribe(client):
    sender = Sender(client)
    sender.unsubscribe('sub1')
    client.send_frame.assert_called_once_with('UNSUBSCRIBE\nid:sub1\n\n\x00')


if __name__ == '__main__':
    pytest.main()
