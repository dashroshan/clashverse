import coc
from secret import (
    discord_token,
    coc_email,
    coc_password,
    mongodb_url,
    coc_keycount,
    useCocPy,
    extensions,
)
from discord.ext import commands
from discord_slash import SlashCommand
from discord import (
    Intents as discord_Intents,
    Activity as discord_Activity,
    ActivityType,
)


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="/",
            case_insensitive=True,
            intents=discord_Intents(guilds=True, members=True),
            help_command=None,
            activity=discord_Activity(
                type=ActivityType.watching, name="/clashverse for help"
            ),
        )
        slash = SlashCommand(self, override_type=True, sync_commands=True)
        if useCocPy == True:
            self.coc = coc.login(
                coc_email,
                coc_password,
                key_names="clashverse",
                key_count=coc_keycount,
                throttle_limit=20,
            )

        for extension in extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f"Error loading {extension} : {e}")

    async def on_ready(self):
        print("Bot is now online!")


if __name__ == "__main__":
    try:
        bot = MyBot()
        bot.run(discord_token)
    except Exception as e:
        print(e)
