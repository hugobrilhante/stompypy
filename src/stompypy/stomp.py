from typing import Optional
from typing import Tuple

from .client import Client
from .listeners import Listener
from .sender import Sender


class Stomp:
    """
    A class representing a Stomp client with basic functionalities.
    """

    def __init__(self, client: Client, sender: Sender):
        """
        Initialize Stomp object with a client and a sender.

        Args:
            client (Client): Stomp client object.
            sender (Sender): Stomp sender object.
        """
        self.client: Client = client
        self.sender: Sender = sender

    @classmethod
    def create_connection(cls, host: str, port: int):
        """
        Create a Stomp object without establishing a connection.

        Args:
            host (str): Hostname or IP address of the Stomp server.
            port (int): Port number of the Stomp server.

        Returns:
            Stomp: Stomp object ready for connection.
        """
        client: Client = Client(host=host, port=port)
        sender: Sender = Sender(client)
        return cls(client, sender)

    def ack(self, message_id: str, transaction: Optional[str] = None) -> None:
        """
        Send an ACK frame.

        Args:
            message_id (str): The identifier of the message to acknowledge.
            transaction (Optional[str]): The transaction identifier if acknowledgment is part of a transaction.
        """
        self.sender.ack(message_id, transaction)

    def abort(self, transaction: str) -> None:
        """
        Send an ABORT frame.

        Args:
            transaction (str): The identifier of the transaction to abort.
        """
        self.sender.abort(transaction)

    def add_listener(self, listener: Listener) -> None:
        """
        Add a listener to receive STOMP frame notifications.

        Args:
            listener (Listener): An object implementing the Listener interface,
                which will receive notifications about STOMP frames.

        Returns:
            None
        """
        self.client.add_listener(listener)

    def begin(self, transaction: str) -> None:
        """
        Send a BEGIN frame.

        Args:
            transaction (str): The identifier of the transaction to begin.
        """
        self.sender.begin(transaction)

    def commit(self, transaction: str) -> None:
        """
        Send a COMMIT frame.

        Args:
            transaction (str): The identifier of the transaction to commit.
        """
        self.sender.commit(transaction)

    def connect(
        self,
        host: Optional[str] = '/',
        accept_version: str = '1.2',
        login: Optional[str] = None,
        passcode: Optional[str] = None,
        heart_beat: Optional[Tuple[int, int]] = (0, 0),
    ) -> None:
        """
        Connect to the Stomp server.

        Args:
            host (Optional[str]): Hostname or IP address of the Stomp server. Defaults to '/'.
            accept_version (str): STOMP protocol versions accepted. Defaults to '1.2'.
            login (Optional[str]): Login username. Defaults to None.
            passcode (Optional[str]): Login password. Defaults to None.
            heart_beat (Optional[Tuple[int, int]]): Tuple of client and server heart-beat settings. Defaults to (0, 0).
        """
        self.client.connect()
        self.sender.connect(host, accept_version, login, passcode, heart_beat)

    def disconnect(self, receipt_id: Optional[str] = None) -> None:
        """
        Send a DISCONNECT frame.

        Args:
            receipt_id (Optional[str]): The identifier of the receipt to wait for before disconnecting.
        """
        self.sender.disconnect(receipt_id)
        self.client.disconnect()

    def nack(self, message_id: str, transaction: Optional[str] = None) -> None:
        """
        Send a NACK frame.

        Args:
            message_id (str): The identifier of the message to reject.
            transaction (Optional[str]): The transaction identifier if rejection is part of a transaction.
        """
        self.sender.nack(message_id, transaction)

    def send(self, destination: str, content_type: str, body: str, transaction: Optional[str] = None) -> None:
        """
        Send a SEND frame.

        Args:
            destination (str): Destination to send the message to.
            content_type (str): MIME type of the message content.
            body (str): Content of the message.
            transaction (Optional[str]): The identifier of the transaction if sending is part of a transaction.
        """
        self.sender.send(destination, content_type, body, transaction)

    def subscribe(self, id: str, destination: str, ack_mode: str) -> None:
        """
        Send a SUBSCRIBE frame.

        Args:
            id (str): Unique identifier for the subscription.
            destination (str): Destination to subscribe to.
            ack_mode (str): Acknowledgement mode, either 'auto', 'client', or 'client-individual'.
        """
        self.sender.subscribe(id, destination, ack_mode)

    def unsubscribe(self, id: str) -> None:
        """
        Send an UNSUBSCRIBE frame.

        Args:
            id (str): The identifier of the subscription to unsubscribe from.
        """
        self.sender.unsubscribe(id)
