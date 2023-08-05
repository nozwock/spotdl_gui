EVENT_CHECK_DELAY = 0.06

from enum import Enum


class MessageType(Enum):
    Success, Error, Progress = range(3)
