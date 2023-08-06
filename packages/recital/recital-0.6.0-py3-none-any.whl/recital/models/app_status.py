from enum import Enum


class AppStatus(str, Enum):
    STARTING = "starting"
    RUNNING = "running"
    ERROR = "error"

    def __str__(self) -> str:
        return str(self.value)
