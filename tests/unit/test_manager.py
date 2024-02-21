from stompypy.managers import EventManager


class MockListener:
    def __init__(self):
        self.events_triggered = []

    def on_event(self, *args, **kwargs):
        self.events_triggered.append(('on_event', args, kwargs))


def test_subscribe():
    event_manager = EventManager()
    listener = MockListener()

    event_manager.subscribe(listener)

    assert listener in event_manager.listeners


def test_unsubscribe():
    event_manager = EventManager()
    listener = MockListener()
    event_manager.subscribe(listener)

    event_manager.unsubscribe(listener)

    assert listener not in event_manager.listeners


def test_notify():
    event_manager = EventManager()
    listener = MockListener()
    event_manager.subscribe(listener)

    event_manager.notify('on_event', 'arg1', kwarg1='value1')

    assert len(listener.events_triggered) == 1
    assert listener.events_triggered[0] == ('on_event', ('arg1',), {'kwarg1': 'value1'})
