from unittest.mock import Mock

import pytest

from src.stompypy.stomp import Stomp


@pytest.fixture
def mock_client():
    return Mock()


@pytest.fixture
def mock_sender():
    return Mock()


@pytest.fixture
def stomp_connection(mock_client, mock_sender):
    return Stomp(mock_client, mock_sender)


def test_ack(stomp_connection):
    stomp_connection.ack('message_id')
    stomp_connection.sender.ack.assert_called_once_with('message_id', None)


def test_abort(stomp_connection):
    stomp_connection.abort('transaction')
    stomp_connection.sender.abort.assert_called_once_with('transaction')


def test_begin(stomp_connection):
    stomp_connection.begin('transaction')
    stomp_connection.sender.begin.assert_called_once_with('transaction')


def test_commit(stomp_connection):
    stomp_connection.commit('transaction')
    stomp_connection.sender.commit.assert_called_once_with('transaction')


def test_disconnect(stomp_connection):
    stomp_connection.disconnect('receipt_id')
    stomp_connection.sender.disconnect.assert_called_once_with('receipt_id')
    stomp_connection.client.disconnect.assert_called_once()


def test_nack(stomp_connection):
    stomp_connection.nack('message_id')
    stomp_connection.sender.nack.assert_called_once_with('message_id', None)


def test_send(stomp_connection):
    stomp_connection.send('destination', 'content_type', 'body')
    stomp_connection.sender.send.assert_called_once_with('destination', 'content_type', 'body', None)


def test_subscribe(stomp_connection):
    stomp_connection.subscribe('id', 'destination', 'ack_mode')
    stomp_connection.sender.subscribe.assert_called_once_with('id', 'destination', 'ack_mode')


def test_unsubscribe(stomp_connection):
    stomp_connection.unsubscribe('id')
    stomp_connection.sender.unsubscribe.assert_called_once_with('id')
