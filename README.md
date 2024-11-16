# Disbeet
Bot for managing a music library via Discord using the beets tool

## Configuration
Create a JSON file with necessary Discord bot login information. Suggested: `discord.py`. Example:
```json
{
    "token": "..."
}
```

## Development
Use `pip install -e '.[dev]'` to install the development environment. I mainly code in neovim. This environment uses mypy for type checking, pylint for linting, black for formatting, and isort for import sorting.

## Sample startup command
Set up a bot using the discord.json file mentioned in the Configuration section
```python
disbeet -t ./discord.json
```
