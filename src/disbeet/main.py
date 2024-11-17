import argparse

# Set up python discord bot
from disbeet._discord.bot import Bot


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="disbeet",
        description="A discord bot used for managing a beets library through discord",
    )

    parser.add_argument("--config", "-c", dest="config", required=True)

    args = parser.parse_args()

    discord_bot = Bot(args.config)
    discord_bot.start_disbeet_bot()
