import logging
import re
import socket
import threading
import time

from .constants import EOL
from .constants import NULL
from .exceptions import ClientError
from .frame import Frame
from .listeners import Listener
from .managers import EventManager

logger = logging.getLogger('stompypy.client')


class Client:
    """
    A client for connecting to a server and exchanging STOMP frames.
    """

    frame_class = Frame

    def __init__(self, host: str, port: int) -> None:
        """
        Initialize the STOMP client.

        Args:
            host (str): The server IP address or hostname.
            port (int): The server port number.
        """
        self.host = host
        self.port = port
        self.connected = threading.Event()
        self.event_manager = EventManager()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) -> None:
        """
        Connect the client to the server.
        """
        try:
            self.socket.connect((self.host, self.port))
            self.connected.set()
            self._start_receive_thread()
            self.event_manager.notify('on_connect')
        except Exception as exc:
            raise ClientError(f'Error connecting to the server: {exc}')

    def disconnect(self) -> None:
        """
        Disconnect the client from the server.
        """
        try:
            self.connected.clear()
            self.event_manager.notify('on_disconnect')
            for thread in threading.enumerate():
                if thread.daemon:
                    thread.join()
            self.socket.close()
        except Exception as exc:
            raise ClientError(f'Error disconnecting from the server: {exc}')

    def send_frame(self, frame: str) -> None:
        """
        Send a frame to the server.

        Args:
            frame (str): The frame to be sent.
        """
        try:
            self.socket.sendall(frame.encode())
        except Exception as exc:
            raise ClientError(f'Error sending frame to the server: {exc}')

    def add_listener(self, listener: Listener) -> None:
        """
        Add a listener for frame events.

        Args:
            listener (Listener): The listener object to be added.
        """
        self.event_manager.subscribe(listener)

    def receive_frames(self) -> None:
        """
        Receive frames from the server.
        """
        try:
            while self.connected.is_set():
                buffer = self._receive()
                if buffer:
                    frame_str = buffer.decode()
                    frame: Frame = self.frame_class.from_string(frame_str)
                    logger.debug('Received frame: %s', frame_str)
                    self._handle_frame(frame)
        except Exception as exc:
            logger.exception(exc)
            raise ClientError(f'Error in receive_frames thread: {exc}')

    def _receive(self) -> bytes:
        """
        Receive data from the socket.

        Returns:
            bytes: Received data.
        """
        try:
            buffer = b''
            while self.connected.is_set():
                chunk = self.socket.recv(4096)
                if not chunk:
                    break
                buffer += chunk
                if NULL.encode() in chunk:
                    break
            return buffer
        except Exception as exc:
            logger.exception(exc)
            raise ClientError(f'Error receiving frames: {exc}')

    def _start_receive_thread(self) -> None:
        """
        Start a daemon thread to receive frames from the server.
        """
        receive_thread = threading.Thread(target=self.receive_frames)
        receive_thread.daemon = True
        receive_thread.start()

    def _handle_frame(self, frame: Frame) -> None:
        """
        Handle received frame.

        Args:
            frame (Frame): Received frame.
        """
        if 'heart-beat' in frame.headers:
            self._parse_heartbeat(frame.headers)
            if self.heartbeat != (0, 0):
                self._start_heartbeat_thread()
        self.event_manager.notify(f'on_{frame.command.lower()}', frame)

    def _parse_heartbeat(self, headers: dict) -> None:
        """
        Parse the frame headers to extract the heart-beat values.

        Args:
            headers (dict): Frame headers.
        """
        try:
            heartbeat_str = headers['heart-beat']
            match = re.match(r'(\d+),(\d+)', heartbeat_str)
            if match:
                self.heartbeat = (int(match.group(1)), int(match.group(2)))
                logger.debug('Heartbeat values: %s', self.heartbeat)
            else:
                logger.warning('Heartbeat values not found in the header.')
        except Exception as exc:
            logger.exception(exc)
            raise ClientError(f'Error parsing heartbeat: {exc}')

    def _start_heartbeat_thread(self) -> None:
        """
        Start a daemon thread to send heartbeats to the server.
        """
        heartbeat_thread = threading.Thread(target=self._send_heartbeat)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()

    def _send_heartbeat(self) -> None:
        """
        Send heartbeats to the server.
        """
        try:
            while self.connected.is_set():
                time.sleep(self.heartbeat[0])
                if self.connected.is_set():
                    try:
                        self.socket.sendall(EOL.encode())
                        logger.debug('Sent heartbeat')
                    except Exception as exc:
                        logger.exception(exc)
                        raise ClientError(f'Error sending heartbeat: {exc}')
        except Exception as exc:
            logger.exception(exc)
            raise ClientError(f'Error in send_heartbeat thread: {exc}')

    def __enter__(self):
        """
        Enter the context manager.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager.
        """
        if exc_type is not None:
            logger.error('An error occurred: %s', exc_value)
        self.disconnect()
