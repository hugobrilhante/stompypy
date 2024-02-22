from typing import Dict
from typing import Optional

from .constants import EOL
from .constants import NULL


class Frame:
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

    def __init__(
        self, command: str = None, headers: Optional[Dict[str, str]] = None, body: Optional[str] = None
    ) -> None:
        self.command: str = command
        self.headers: Optional[Dict[str, str]] = headers
        self.body: str = body

    @classmethod
    def from_string(cls, frame_str: str) -> 'Frame':
        """
        Generate a Frame object from a string formatted according to the STOMP frame specification.

        Args:
            frame_str (str): The string representing the STOMP frame.

        Returns:
            Frame: An instance of Frame class representing the parsed STOMP frame.
        """
        parts = frame_str.split(EOL * 2)
        command_headers = parts[0]
        body = parts[1].rstrip(NULL)
        command, *headers = command_headers.split(EOL)
        headers = dict(header.split(':') for header in headers)
        return cls(command, headers, body)

    def to_string(self) -> str:
        """
        Generate the string representation of the STOMP frame.

        """
        frame_lines = [self.command]
        if self.headers:
            frame_lines.extend([f'{key}:{value}' for key, value in self.headers.items()])
        if self.body:
            frame_lines.extend(['', self.body])
        frame_lines.extend(['', NULL])
        return EOL.join(frame_lines)
