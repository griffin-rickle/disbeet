from abc import ABC, abstractmethod

from discord import Message


class Command(ABC):
    def __init__(self, message: Message):
        self.message = message

    # TODO: Implement CommandResult
    @abstractmethod
    def execute(self) -> None:
        pass
