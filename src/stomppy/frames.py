from typing import Dict
from typing import Optional

from stomppy.constants import EOL
from stomppy.constants import NULL


class FrameStomp(str):
    """
    Represents a generic STOMP frame.

    This class provides a representation of a generic STOMP frame, allowing for easy manipulation
    and creation of frames according to the STOMP protocol specification. It supports instantiation
    from a command, optional headers, and an optional body. Additionally, it can parse a string
    formatted according to the STOMP frame specification.

    Args:
        command (str): The command of the STOMP frame.
        headers (Optional[Dict[str, str]]): Optional headers of the STOMP frame.
        body (Optional[str]): Optional body of the STOMP frame.

    Attributes:
        command (str): The command of the STOMP frame.
        headers (Optional[Dict[str, str]]): The headers of the STOMP frame.
        body (Optional[str]): The body of the STOMP frame.

    References:
        - STOMP 1.2 Specification: https://stomp.github.io/stomp-specification-1.2.html
    """

    command: str
    headers: Optional[Dict[str, str]]
    body: Optional[str]

    def __new__(cls, command: str = None, headers: Optional[Dict[str, str]] = None, body: Optional[str] = None) -> str:
        frame_lines = [command]
        if headers:
            frame_lines.extend([f'{key}:{value}' for key, value in headers.items()])
        if body:
            frame_lines.extend(['', body])
        frame_lines.extend(['', NULL])
        frame_string = EOL.join(frame_lines)
        instance = super().__new__(cls, frame_string)
        instance.command = command
        instance.headers = headers
        instance.body = body
        return instance
