from discord.ext import commands
from utility.errorimage import errorimg
from discord_slash import cog_ext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import (
    create_select,
    create_select_option,
    create_actionrow,
    create_button,
)
from secret import testguild, statguild
from discord import Embed as discord_Embed, File as discord_File
from discord.utils import find as utils_find
from io import StringIO
import topgg

helpselectimgs = {
    "desc": "To learn how to use the different features available on ClashVerse, use the selection box below. Feel free to join the support server if you need additional assistance.\n\n**[Invite ClashVerse to another server](https://clashverse.dashroshan.com/i)\n[Join support server](https://clashverse.dashroshan.com/s)**",
    "0": "https://i.imgur.com/Qzexa94.jpg",
    "1": "https://i.imgur.com/hZTk9EP.jpg",
    "2": "https://i.imgur.com/5ZjNWpg.jpg",
    "3": "https://i.imgur.com/LoVr2oF.jpg",
    "4": "https://i.imgur.com/VrT68KY.jpg",
    "5": "https://i.imgur.com/orTMicM.jpg",
    "6": "https://i.imgur.com/TsEi5EP.jpg",
    "7": "https://i.imgur.com/kqXKapk.jpg",
    "8": "https://i.imgur.com/eiI79eJ.jpg",
}


class Generalcmnds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.topggpy = topgg.DBLClient(
            bot,
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijg2NjczMzAyNjY2NzAwMzkwNCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjI3NDYzNjA2fQ.0t94CrfFGIi15dRVDoFcmgKT5TNmX6Q5RJMALFWTNtc",
        )

    async def aboutmsg(self, ctx):
        select = create_select(
            options=[
                create_select_option(
                    "Save Default Clan",
                    description="Set own, channel, category or server default clan",
                    value="1",
                ),
                create_select_option(
                    "Clear Default Clan",
                    description="Clear a default clan that was previously saved",
                    value="2",
                ),
                # create_select_option(
                #     "Trader Cycle",
                #     description="Find next occurrence of any item in trader cycle",
                #     value="3",
                # ),
                create_select_option(
                    "War Stats",
                    description="Get stats of your ongoing regular or league wars",
                    value="4",
                ),
                create_select_option(
                    "Clan Stats",
                    description="Get the townhall comp of your clan with avg stats",
                    value="5",
                ),
                create_select_option(
                    "ZapQuake Combos",
                    description="Find ZQ combos to take down any defense or hero",
                    value="6",
                ),
                create_select_option(
                    "Active Super Troops",
                    description="Find your clan mates having any active super troop",
                    value="7",
                ),
                create_select_option(
                    "Embed and Button Roles",
                    description="Create discord embeds with or without button roles",
                    value="8",
                ),
            ],
            placeholder="Select a feature to learn how to use it",
            min_values=1,
            max_values=1,
            custom_id="helpselect",
        )
        embed = discord_Embed(
            title="ClashVerse | Clash of Clans discord bot",
            url="https://clashverse.dashroshan.com",
            color=0x108ADF,
            description=helpselectimgs["desc"],
        )
        embed.set_image(url=helpselectimgs["0"])
        await ctx.send(embed=embed, components=[create_actionrow(select)])

    @commands.Cog.listener()
    async def on_component(self, ctx):
        if ctx.custom_id == "helpselect":
            embed = discord_Embed(
                title="ClashVerse | Clash of Clans discord bot",
                url="https://clashverse.dashroshan.com",
                color=0x108ADF,
                description=helpselectimgs["desc"],
            )
            embed.set_image(url=helpselectimgs[ctx.selected_options[0]])
            await ctx.edit_origin(embed=embed)

    @cog_ext.cog_slash(
        name="clashverse",
        description="ClashVerse user guide, invite and support server",
        guild_ids=testguild,
    )
    async def cvabout(self, ctx):
        await ctx.defer()
        await self.aboutmsg(ctx)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        raise error

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logc = self.bot.get_channel(824268574273175593)
        botc, userc = 0, 0
        for m in guild.members:
            if m.bot == True:
                botc += 1
            else:
                userc += 1
        await logc.send(
            f"Joined {guild.name} with {userc} users and {botc} bots!\n{guild.id} | Servers : {len(self.bot.guilds)}"
        )
        for channel in guild.text_channels:
            if (
                channel.permissions_for(guild.me).attach_files
                and channel.permissions_for(guild.me).send_messages
            ):
                await errorimg(
                    "It's an honour to be welcomed here Chief! To access the user guide send /clashverse",
                    2,
                    channel,
                    True,
                )
                return
        await self.topggpy.post_guild_count()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        logc = self.bot.get_channel(824268574273175593)
        botc, userc = 0, 0
        for m in guild.members:
            if m.bot == True:
                botc += 1
            else:
                userc += 1
        await logc.send(
            f"Left {guild.name} with {userc} users and {botc} bots!\n{guild.id} | Servers : {len(self.bot.guilds)}"
        )
        await self.topggpy.post_guild_count()

    @cog_ext.cog_slash(
        name="stats",
        description="ClashVerse bot stats",
        guild_ids=statguild,
    )
    async def imgstats(self, ctx):
        servers = 0
        users = 0
        for guild in self.bot.guilds:
            servers += 1
            users += guild.member_count
        ping = round(self.bot.latency * 1000)
        await errorimg(
            f"ClashVerse is being\nused by {users} members\nof {servers} servers Chief!\nPing is {ping}ms",
            2,
            ctx,
            False,
        )


def setup(bot):
    bot.add_cog(Generalcmnds(bot))
    print("General cog loaded!")
