import json
from pathlib import Path
from typing import Any, Dict

import discord
from pydantic import BaseModel


class BotConfig(BaseModel):
    app_id: str
    public_key: str
    token: str
    import_channel_id: int


class Bot(discord.Client):
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

        super().__init__(intents=self._intents)

    def initialize_intents(self) -> discord.Intents:
        intents = discord.Intents.default()
        intents.message_content = True
        return intents

    def start_disbeet_bot(self) -> None:
        super().run(self.config.token)

    async def on_ready(self) -> None:
        print("bot ready!")

    async def on_message(self, message: discord.Message) -> None:
        if message.channel.id == self.config.import_channel_id:
            await self.process_message(message)

    async def process_message(self, message: discord.Message) -> None:
        print(f"Received message: {message.author}: {message.content}")
