import json
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

from discord import Client, Intents, Message, TextChannel, Thread
from pydantic import BaseModel, field_validator

from disbeet._discord.import_status import ImportContext, ImportStatus


class BotConfig(BaseModel):
    app_id: str
    public_key: str
    token: str
    guild_id: int
    import_channel_id: int
    beets_config: Path
    new_imports_dir: Path

    @field_validator("beets_config", "new_imports_dir", mode="before")
    @classmethod
    def to_pathlike(cls, v: str) -> Path:
        return Path(v)


class Bot(Client):

    import_channel: TextChannel
    state_message: Message
    import_threads: Dict[str, Tuple[Message, Thread]]

    def __init__(self, config_filepath: str):
        self._intents = self.initialize_intents()
        config_path = Path(config_filepath)
        if not config_path.exists():
            raise RuntimeError(f"No file exists at config_filepath: {config_filepath}")

        config: str
        try:
            config = config_path.read_text("utf-8").strip()
        except Exception as e:
            raise RuntimeError(
                f"Cannot read contents of config_filepath: {config_filepath}"
            ) from e

        config_dict: Dict[str, Any]
        self.import_contexts: Dict[str, ImportContext] = {}
        try:
            config_dict = json.loads(config)
        except Exception as e:
            raise RuntimeError(
                f"config_filepath contains invalid JSON: {config_filepath}"
            ) from e

        # TODO: Why does this not like when the type of config_dict is Dict[str, Union[str, int]]?
        self.config: BotConfig = BotConfig(**config_dict)
        super().__init__(intents=self._intents)

    def initialize_intents(self) -> Intents:
        intents = Intents.default()
        intents.message_content = True
        return intents

    def start_disbeet_bot(self) -> None:
        super().run(self.config.token)

    async def on_ready(self) -> None:
        self.import_channel = await self.get_import_channel()
        self.state_message = await self.get_state_message()
        await self.publish_filesystem_udpate()
        print("bot ready!")

    async def on_message(self, message: Message) -> None:
        if message.author.bot:
            return
        if (
            message.channel.id == self.config.import_channel_id
            and message.content.split()[0] == "!tag"
        ):
            await self.process_tagstart_message(message)
        if (
            isinstance(message.channel, Thread)
            and message.channel.name in self.import_threads
        ):
            await self.process_tagging_thread_message(message.channel.name, message)

    async def process_tagging_thread_message(
        self, thread_name: str, message: Message
    ) -> None:
        if self.import_contexts[thread_name].status == ImportStatus.UNSTARTED:
            # Expecting `manual` or `auto` here
            pass
        else:
            # Expecting response to `manual` or `auto` here
            pass

    async def process_tagstart_message(self, message: Message) -> None:
        print(f"Received import message: {message.author}: {message.content}")
        import_dir = " ".join(message.content.split()[1:])
        existing_thread_info = self.import_threads.get(import_dir)
        if existing_thread_info is not None:
            creation_message, existing_thread = existing_thread_info
            await message.reply(
                f"An import thread was already started by {creation_message.author}: "
                f"<#{existing_thread.id}>"
            )
            return
        import_thread = await self.import_channel.create_thread(name=f"{import_dir}")
        self.import_contexts[import_dir] = ImportContext(
            import_path=Path(self.config.new_imports_dir / import_dir),
            initiating_message=message,
            thread=import_thread,
        )
        thread_opening_message = f"""This is a thread for importing the directory {import_dir}
This import was initiated by <@{message.author.id}>
Your options are:
- `manual`: This command will prompt you for an Artist, Album Name, and 
Year for the album. After gathering that information, it will apply the 
changes and use the filenames as song names (minus `.flac` and `.mp3`)
- `auto`: I'm not really sure how this will work but there's existing 
logic in the autotagger which I will look into and try to tap into.

The contents of this directory are:
```{self.dir_contents(import_dir)}```
"""
        await self.send_thread_message(import_thread, thread_opening_message)

    async def send_thread_message(self, thread: Thread, message_content: str) -> None:
        await thread.send(content=message_content)

    def dir_contents(self, import_dir: str) -> str:
        import_path = Path(self.config.new_imports_dir / import_dir)
        return "\n\t" + "\n\t".join([file.name for file in import_path.iterdir()])

    async def publish_filesystem_udpate(self) -> None:
        new_import_subdirs = await self.get_filesystem_listing()
        state_message = await self.get_state_message()
        print(f"found state message with content {state_message.content}")
        await state_message.edit(
            content=f"""Directories available for import:\n```{'\n'.join(new_import_subdirs)}```"""
        )

    async def get_import_channel(self) -> TextChannel:
        my_guild = self.guilds[0]
        if my_guild is None:
            raise RuntimeError(f"Could not find server with id {self.config.guild_id}")

        channel = my_guild.get_channel(self.config.import_channel_id)
        if not channel:
            raise RuntimeError(
                f"Could not find channel with id {self.config.import_channel_id}"
            )

        if not isinstance(channel, TextChannel):
            raise RuntimeError(
                f"Channel with given ID is not a text channel {self.config.import_channel_id}"
            )

        return channel

    async def get_state_message(self) -> Message:
        pinned_messages: List[Message] = await self.import_channel.pins()
        if len(pinned_messages) > 1:
            raise RuntimeError(
                "More than one pinned message found in import channel "
                f"{self.import_channel.name}"
            )
        if len(pinned_messages) == 0:
            raise RuntimeError(
                f"No pinned messages found in channel {self.import_channel.name}"
            )
        return pinned_messages[0]

    async def get_filesystem_listing(self) -> Sequence[str]:
        return sorted(
            [
                directory.name
                for directory in self.config.new_imports_dir.iterdir()
                if directory.is_dir()
            ]
        )
