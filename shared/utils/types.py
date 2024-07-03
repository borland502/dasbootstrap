"""Types for Dasbootstrap."""

import threading


class SingletonMeta(type):
    """Metaclass to ensure a single instance of the class."""

    _instance = None
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        """Create a single instance of the class and return that instance thereafter."""
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
