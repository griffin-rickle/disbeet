from enum import Enum
from pathlib import Path
from typing import Boolean, List, Optional, Tuple

from discord import Message, Thread

from disbeet._discord.command import Command


class ImportMethod(Enum):
    MANUAL = 1
    AUTO = 2


class ImportStatus(Enum):
    UNSTARTED = 1
    STARTED = 2


class ImportContext:
    def __init__(
        self,
        import_path: Path,
        thread: Thread,
        initiating_message: Message,
        status: ImportStatus = ImportStatus.UNSTARTED,
        method: Optional[ImportMethod] = None,
    ):
        self.import_path = import_path
        self.thread = thread
        self.intiating_message = initiating_message
        self.status = status
        self.method = method
        self.history: List[Tuple[Command, Boolean]] = []

    # def add_history_step(self, message: Message, command: Command) -> None:
    #     self.history.append((message, command))
