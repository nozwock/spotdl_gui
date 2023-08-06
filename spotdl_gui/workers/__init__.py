from enum import Enum

EVENT_CHECK_DELAY = 0.06


class MessageType(Enum):
    Success, Error, Progress = range(3)
