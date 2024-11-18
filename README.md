# Disbeet
Bot for managing a music library via Discord using the beets tool

## Configuration
Create a JSON file with necessary Discord bot login information. Suggested: `discord.json`. Example:
```json
{
    "token": "..."
}
```

## Discord Output
The bot will look in the configured channel for a single pinned message. it will crash if there is more than one pinned message. It will assume that it can edit this message. This message will be referred to as the State Message. This is where the state of the new imports will be kept. Users in the channel may examine the State Message and use the `!tag <directory> command to start a tagging session for the given directory name. This will prompt the bot to start a new thread with the person who started the tagging session. More to come about what happens after that. 

## Development
I use python's venv module to create a virtual environment for development: `python -m venv venv; . venv/bin/activate`. Then use `pip install -e '.[dev]'` to install the development environment. I mainly code in neovim. This environment uses mypy for type checking, pylint for linting, black for formatting, and isort for import sorting.

## Sample startup command
Set up a bot using the discord.json file mentioned in the Configuration section
```bash
python -m venv venv
. venv/bin/activate
disbeet -c ./discord.json
```
