from beets import config, importer, plugins
import discord


class Autobeets(object):
    class AutoImportSession(importer.ImportSession):
        def should_resume(self, path):
            return False

        def choose_match(self, task):
            if task.rec == Recommendation.string:
                return task.candidates[0]
            else:
                return importer.action.SKIP

class DisbeetClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Got a message: {message.content}')
        print(f'channel: {message.channel.id}')
        if message.author.bot:
            return
        if message.channel.id == 1110361825830256761:
            await message.reply(content="i'm here now")
            return


def get_token():
    with open('discord_token.txt') as f:
        return f.read()


intents = discord.Intents.default()
intents.auto_moderation = False
intents.auto_moderation_configuration = False
intents.auto_moderation_execution = False
intents.bans = False
intents.dm_messages = False
intents.dm_reactions = False
intents.dm_typing = False
intents.emojis = False
intents.emojis_and_stickers = False
intents.guild_messages = False
intents.guild_reactions = False
intents.guild_scheduled_events = False
intents.guild_typing = False
intents.guilds = False
intents.integrations = False
intents.invites = False
intents.members = False
intents.presences = False
intents.reactions = False
intents.typing = False
intents.value = False
intents.voice_states = False
intents.webhooks = False

intents.message_content = True
intents.messages = True

client = DisbeetClient(intents=intents)
client.run(get_token())
