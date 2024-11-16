import argparse
from typing import NoReturn

# Set up python discord bot
from disbeet._beet.controller import instantiate_beet_album, instantiate_beet_item


# def main() -> NoReturn:
def main() -> None:
    parser = argparse.ArgumentParser(
        prog="disbeet",
        description="A discord bot used for managing a beets library through discord",
    )

    parser.add_argument("--import-dir,-i", dest="new_imports_directory")
    parser.add_argument("--beets-config,-c", dest="beets_config")

    args = parser.parse_args()
    print(f"New Imports Directory: {args.new_imports_directory}")
    print(f"Beets config configuration: {args.beets_config}")
