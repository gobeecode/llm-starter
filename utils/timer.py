import time

class TimerError(Exception):
    """Custom exception for Timer class"""
    pass

class Timer:
    _timers = {}

    @classmethod
    def start(cls, name="default"):
        """Start a named timer"""
        if name in cls._timers and cls._timers[name]["start"] is not None:
            raise TimerError(f"Timer '{name}' is already running.")
        cls._timers[name] = {"start": time.perf_counter(), "end": None, "elapsed": None}

    @classmethod
    def stop(cls, name="default"):
        """Stop a named timer"""
        if name not in cls._timers or cls._timers[name]["start"] is None:
            raise TimerError(f"Timer '{name}' is not running.")
        cls._timers[name]["end"] = time.perf_counter()
        cls._timers[name]["elapsed"] = cls._timers[name]["end"] - cls._timers[name]["start"]

    @classmethod
    def elapsed(cls, name="default"):
        """Return elapsed time for a timer"""
        if name not in cls._timers or cls._timers[name]["elapsed"] is None:
            raise TimerError(f"Timer '{name}' has not been stopped yet.")
        return cls._timers[name]["elapsed"]

    @classmethod
    def report(cls):
        """Prints a report of all stopped timers"""
        print("Timer Report:")
        for name, times in cls._timers.items():
            if times["elapsed"] is not None:
                print(f" - {name}: {times['elapsed']:.6f} seconds")
            else:
                print(f" - {name}: still running or not stopped")