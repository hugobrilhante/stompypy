from typing import Dict
from typing import Optional
from typing import Tuple

from .frame import Frame


class Sender:
    """
    Represents a STOMP frame sender.

    This class provides methods to generate various STOMP client frames according to the STOMP 1.2 specification
    and send them to the server using a provided `send_frame` method from a client.

    References:
        - STOMP 1.2 Specification: https://stomp.github.io/stomp-specification-1.2.html
    """

    frame_class = Frame

    def __init__(self, client):
        self.client = client

    def send_frame(self, frame: str) -> None:
        """
        Sends the provided frame to the server using the client's send_frame method.

        Args:
            frame (str): The STOMP frame to send to the server.
        """
        self.client.send_frame(frame)

    def _generate_frame(
        self, command: str, headers: Optional[Dict[str, str]] = None, body: Optional[str] = None
    ) -> str:
        """
        Generate a STOMP frame.

        Args:
            command (str): The command of the STOMP frame.
            headers (Optional[Dict[str, str]]): Optional headers of the STOMP frame.
            body (Optional[str]): Optional body of the STOMP frame.

        Returns:
            str: The generated STOMP frame.
        """
        return self.frame_class(command, headers, body).to_string()

    def ack(self, message_id: str, transaction: Optional[str] = None) -> None:
        """
        Generate and send an ACK frame.

        Args:
            message_id (str): The identifier of the message to acknowledge.
            transaction (Optional[str]): The transaction identifier if acknowledgment is part of a transaction.
        """
        frame = self._generate_frame(
            'ACK', {'id': message_id, 'transaction': transaction} if transaction else {'id': message_id}
        )
        self.send_frame(frame)

    def abort(self, transaction: str) -> None:
        """
        Generate and send an ABORT frame to roll back a transaction.

        Args:
            transaction (str): The identifier of the transaction to abort.
        """
        frame = self._generate_frame('ABORT', {'transaction': transaction})
        self.send_frame(frame)

    def begin(self, transaction: str) -> None:
        """
        Generate and send a BEGIN frame to start a transaction.

        Args:
            transaction (str): The identifier of the transaction to begin.
        """
        frame = self._generate_frame('BEGIN', {'transaction': transaction})
        self.send_frame(frame)

    def commit(self, transaction: str) -> None:
        """
        Generate and send a COMMIT frame to commit a transaction.

        Args:
            transaction (str): The identifier of the transaction to commit.
        """
        frame = self._generate_frame('COMMIT', {'transaction': transaction})
        self.send_frame(frame)

    def connect(
        self,
        host: Optional[str] = '/',
        accept_version: str = '1.2',
        login: Optional[str] = None,
        passcode: Optional[str] = None,
        heart_beat: Optional[Tuple[int, int]] = (0, 0),
    ) -> None:
        """
        Generate and send a CONNECT or STOMP frame.

        Args:
            host (str): The name of the virtual host to connect to.
            accept_version (str): The versions of the STOMP protocol the client supports.
            login (Optional[str]): The user identifier used to authenticate against a secured STOMP server.
            passcode (Optional[str]): The password used to authenticate against a secured STOMP server.
            heart_beat (Optional[Tuple[int, int]]): The Heart-beating settings.
        """
        headers = {'host': host, 'accept-version': accept_version}
        if login:
            headers['login'] = login
        if passcode:
            headers['passcode'] = passcode
        if heart_beat:
            headers['heart-beat'] = f'{heart_beat[0]},{heart_beat[1]}'
        frame = self._generate_frame('CONNECT', headers)
        self.send_frame(frame)

    def disconnect(self, receipt_id: Optional[str] = None) -> None:
        """
        Generate and send a DISCONNECT frame to disconnect from the server gracefully.

        Args:
            receipt_id (Optional[str]): The identifier for the receipt of the disconnect operation.
        """
        headers = {'receipt': receipt_id} if receipt_id else None
        frame = self._generate_frame('DISCONNECT', headers)
        self.send_frame(frame)

    def nack(self, message_id: str, transaction: Optional[str] = None) -> None:
        """
        Generate and send a NACK frame.

        Args:
            message_id (str): The identifier of the message to negatively acknowledge.
            transaction (Optional[str]): The transaction identifier if negative acknowledgment is part of a transaction.
        """
        frame = self._generate_frame(
            'NACK', {'id': message_id, 'transaction': transaction} if transaction else {'id': message_id}
        )
        self.send_frame(frame)

    def send(self, destination: str, content_type: str, body: str, transaction: Optional[str] = None) -> None:
        """
        Generate and send a SEND frame.

        Args:
            destination (str): The destination to send the message.
            content_type (str): The content type of the message.
            body (str): The body of the message.
            transaction (Optional[str]): The transaction identifier if message is part of a transaction.
        """
        headers = (
            {'destination': destination, 'content-type': content_type, 'transaction': transaction}
            if transaction
            else {'destination': destination, 'content-type': content_type}
        )
        frame = self._generate_frame('SEND', headers, body)
        self.send_frame(frame)

    def subscribe(self, id: str, destination: str, ack_mode: str) -> None:
        """
        Generate and send a SUBSCRIBE frame.

        Args:
            id (str): The identifier for the subscription.
            destination (str): The destination to subscribe.
            ack_mode (str): The acknowledgment mode.
        """
        headers = {'id': id, 'destination': destination, 'ack': ack_mode}
        frame = self._generate_frame('SUBSCRIBE', headers)
        self.send_frame(frame)

    def unsubscribe(self, id: str) -> None:
        """
        Generate and send an UNSUBSCRIBE frame.

        Args:
            id (str): The identifier for the subscription to unsubscribe.
        """
        frame = self._generate_frame('UNSUBSCRIBE', {'id': id})
        self.send_frame(frame)
