from .frame import Frame


class Listener:
    """
    Interface for STOMP frame listeners.
    """

    def on_disconnect(self) -> None:
        """
        Invoked when a DISCONNECT frame is sent.
        """
        pass

    def on_connect(self) -> None:
        """
        Invoked when a CONNECT frame is sent.
        """
        pass

    def on_connected(self, frame: Frame) -> None:
        """
        Invoked when a CONNECTED frame is received.

        Args:
            frame (Frame): The CONNECTED frame.
        """
        pass

    def on_message(self, frame: Frame) -> None:
        """
        Invoked when a MESSAGE frame is received.

        Args:
            frame (Frame): The MESSAGE frame.
        """
        pass

    def on_error(self, frame: Frame) -> None:
        """
        Invoked when an ERROR frame is received.

        Args:
            frame (Frame): the ERROR frame.
        """
        pass
