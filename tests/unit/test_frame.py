import pytest
from stomppy.frame import Frame


def test_frame_creation():
    command = 'COMMAND'
    headers = {'header1': 'value1', 'header2': 'value2'}
    body = 'body message'
    frame = Frame(command, headers, body)
    assert frame.command == command
    assert frame.headers == headers
    assert frame.body == body
    expected_frame_string = 'COMMAND\nheader1:value1\nheader2:value2\n\nbody message\n\n\x00'
    assert frame == expected_frame_string


def test_frame_creation_without_headers_and_body():
    command = 'COMMAND'
    frame = Frame(command)
    assert frame.command == command
    assert frame.headers is None
    assert frame.body is None
    expected_frame_string = 'COMMAND\n\n\x00'
    assert frame == expected_frame_string


def test_frame_creation_without_body():
    command = 'COMMAND'
    headers = {'header1': 'value1', 'header2': 'value2'}
    frame = Frame(command, headers)
    assert frame.command == command
    assert frame.headers == headers
    assert frame.body is None
    expected_frame_string = 'COMMAND\nheader1:value1\nheader2:value2\n\n\x00'
    assert frame == expected_frame_string


if __name__ == '__main__':
    pytest.main()
