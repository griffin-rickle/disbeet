import abc
import json
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, cast

from discord import Client, Intents, Message, TextChannel
from pydantic import BaseModel, field_validator


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
        try:
            config_dict = json.loads(config)
        except Exception as e:
            raise RuntimeError(
                f"config_filepath contains invalid JSON: {config_filepath}"
            ) from e

        # TODO: Why does this not like when the type of config_dict is Dict[str, Union[str, int]]?
        self.config: BotConfig = BotConfig(**config_dict)
        self.state_message = self.get_state_message()
        super().__init__(intents=self._intents)

    def initialize_intents(self) -> Intents:
        intents = Intents.default()
        intents.message_content = True
        return intents

    def start_disbeet_bot(self) -> None:
        super().run(self.config.token)

    async def on_ready(self) -> None:
        await self.publish_filesystem_udpate()
        print("bot ready!")

    async def on_message(self, message: Message) -> None:
        if message.channel.id == self.config.import_channel_id:
            await self.process_message(message)

    async def process_message(self, message: Message) -> None:
        print(f"Received message: {message.author}: {message.content}")

    async def publish_filesystem_udpate(self) -> None:
        # new_import_subdirs = await self.get_filesystem_listing()
        # state_message = await self.get_state_message()
        channel = await self.get_import_channel()
        await channel.send("hello")

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

    async def get_state_message(self) -> Optional[Message]:
        return None
        # return await discord.utils.get(
        #     self.get_guild(self.config.guild_id)
        #     .get_channel(self.config.import_channel_id)
        #     .history(limit=1, oldest_first=True)
        # )

    async def get_filesystem_listing(self) -> Sequence[Path]:
        return [
            directory
            for directory in self.config.new_imports_dir.iterdir()
            if directory.is_dir()
        ]
