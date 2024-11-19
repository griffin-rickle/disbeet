from pathlib import Path
from typing import Dict, List, Optional, Tuple

from discord import Message, Thread


class Transform:
    def __init__(
        self, filepath: Path, field: str, new_value: str, metadata_message: Message
    ):
        self.filepath = filepath
        self.tx_from = field
        self.tx_to = new_value
        self.meta_message = metadata_message


class ImportTransforms:
    def __init__(
        self,
        import_path: Path,
        thread: Thread,
        initiating_message: Message,
        existing_transforms: Dict[str, Transform] = {},
    ):
        self.import_path = import_path
        self.thread = thread
        self.initiating_message = initiating_message
        self.transforms: List[Tuple[Transform, bool]] = []

    def register_transform(self, metadata_message: Optional[Message] = None) -> None:
        pass
