import logging
import re
import socket
import threading
import time
from typing import Tuple

from stomppy.constants import EOL
from stomppy.constants import NULL

logger = logging.getLogger(__name__)


class Client:
    """
    A client for connecting to a server and exchanging STOMP frames.

    """

    connected: bool = False
    heartbeat: Tuple[int, int] = (0, 0)

    def __init__(self, host: str, port: int) -> None:
        """
        Initialize the STOMP client.

        Args:
            host (str): The server IP address or hostname.
            port (int): The server port number.
        """
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_thread = threading.Thread(target=self.receive_frames, daemon=True)
        self.receive_thread.start()

    def connect(self) -> None:
        """
        Connect the client to the server.
        """
        self.connected = True
        self.socket.connect((self.host, self.port))

    def disconnect(self) -> None:
        """
        Disconnect the client from the server.
        """
        self.connected = False
        self.socket.close()

    def send_frame(self, frame: str) -> None:
        """
        Send a frame to the server.

        Args:
            frame (str): The frame to be sent.
        """
        self.socket.sendall(frame.encode())

    def receive_frames(self) -> None:
        """
        Receive frames from the server.
        """
        while self.connected:
            buffer = b''
            while self.connected:
                chunk = self.socket.recv(4096)
                if not chunk:
                    break
                buffer += chunk
                if NULL.encode() in chunk:
                    break
            if buffer:
                logger.debug('Received frame: %s', buffer.decode())
                if 'heart-beat' in buffer.decode():
                    self.parse_heartbeat(buffer)

    def parse_heartbeat(self, buffer: bytes) -> None:
        """
        Parse the frame header to extract the heart-beat values.

        Args:
            buffer (bytes): The buffer containing the received frame.
        """
        match = re.search(r'heart-beat:(\d+),(\d+)', buffer.decode())
        if match:
            self.heartbeat = (int(match.group(1)), int(match.group(2)))
            logger.debug('Heartbeat values: %s', self.heartbeat)
            heartbeat_thread = threading.Thread(target=self.send_heartbeat, daemon=True)
            heartbeat_thread.start()
        else:
            logger.warning('Heartbeat values not found in the header.')

    def send_heartbeat(self) -> None:
        """
        Send heartbeats to the server.
        """
        while self.heartbeat == (0, 0) and self.connected:
            time.sleep(1)
        while self.connected:
            time.sleep(self.heartbeat[0])
            if self.connected:
                self.socket.sendall(EOL.encode())
                logger.debug('Sent heartbeat')
