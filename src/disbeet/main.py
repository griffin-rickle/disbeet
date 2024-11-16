import argparse

# Set up python discord bot
from disbeet._discord.bot import Bot


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="disbeet",
        description="A discord bot used for managing a beets library through discord",
    )

    parser.add_argument("--import-dir", "-i", dest="new_imports_directory")
    parser.add_argument("--beets-config", "-b", dest="beets_config")
    parser.add_argument("--discord-config", "-d", dest="discord_config", required=True)

    args = parser.parse_args()
    print(f"New Imports Directory: {args.new_imports_directory}")
    print(f"Beets config configuration: {args.beets_config}")
    print(f"Discord config filepath: {args.discord_config}")

    discord_bot = Bot(args.discord_config)
    discord_bot.start_disbeet_bot()
