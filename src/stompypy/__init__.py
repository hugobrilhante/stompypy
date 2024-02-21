import importlib.metadata

__version__ = importlib.metadata.version(__package__ or __name__)

from .listeners import Listener
from .logging_config import setup_logging
from .stomp import Stomp

setup_logging()

__all__ = ['Stomp', 'Listener']
