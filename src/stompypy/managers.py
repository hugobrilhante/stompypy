from typing import List

from .listeners import Listener


class EventManager:
    """
    A simple event manager to handle subscriptions and notifications.

    Attributes:
        listeners (List[Listener]): A list to store subscribed listeners.
    """

    def __init__(self):
        """
        Initializes the EventManager with an empty list of listeners.
        """
        self.listeners: List[Listener] = []

    def subscribe(self, listener):
        """
        Subscribe a listener to the event manager.

        Args:
            listener: An object that implements the desired event methods.

        Returns:
            None
        """
        self.listeners.append(listener)

    def unsubscribe(self, listener):
        """
        Unsubscribe a listener from the event manager.

        Args:
            listener: An object that was previously subscribed.

        Returns:
            None
        """
        self.listeners.remove(listener)

    def notify(self, event, *args, **kwargs):
        """
        Notify all subscribed listeners of an event.

        Args:
            event: A string representing the event to be triggered.
            *args: Additional positional arguments to be passed to listeners.
            **kwargs: Additional keyword arguments to be passed to listeners.

        Returns:
            None
        """
        for listener in self.listeners:
            if hasattr(listener, event):
                getattr(listener, event)(*args, **kwargs)
