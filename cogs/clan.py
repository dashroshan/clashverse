from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from utility.clanprocess import (
    clansavefn,
    clanclearfn,
    clansuperfn,
    clanstatsfn,
    clanwar_scoreboardfn,
    clanwar_lineupfn,
)
from discord_slash.utils.manage_commands import create_option, create_choice
from secret import testguild


class Clan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="clan-war",
        guild_ids=testguild,
        description="Get the current regular or league war stats",
        options=[
            create_option(
                name="show",
                description="Select the war stat you want to see from the list above",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="Scoreboard", value="1"),
                    create_choice(name="Lineup", value="2"),
                ],
            ),
            create_option(
                name="tag",
                description="Enter the clan tag with #",
                option_type=3,
                required=False,
            ),
        ],
    )
    async def _clanwar(self, ctx: SlashContext, show: str, tag: str = ""):
        if show == "1":
            await ctx.defer()
            await clanwar_scoreboardfn(ctx, tag, self.bot.coc)
        elif show == "2":
            await ctx.defer()
            await clanwar_lineupfn(ctx, tag, self.bot.coc)

    @cog_ext.cog_slash(
        name="clan-stats",
        guild_ids=testguild,
        description="Townhall composition of your clan with avg stats",
        options=[
            create_option(
                name="tag",
                description="Enter the clan tag with #",
                option_type=3,
                required=False,
            )
        ],
    )
    async def _clancomp(self, ctx: SlashContext, tag: str = ""):
        await ctx.defer()
        await clanstatsfn(ctx, tag, self.bot.coc)

    @cog_ext.cog_slash(
        name="clan-save",
        guild_ids=testguild,
        description="Set own, channel, category or server default clan",
        options=[
            create_option(
                name="tag",
                description="Enter the clan tag with #",
                option_type=3,
                required=True,
            ),
            create_option(
                name="default_for",
                description="Select what should this clan be the default for",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="Only me", value="1"),
                    create_choice(name="This channel", value="2"),
                    create_choice(name="This category", value="3"),
                    create_choice(name="Entire server", value="4"),
                ],
            ),
        ],
    )
    async def _clansave(self, ctx: SlashContext, tag: str, default_for: str):
        await ctx.defer()
        await clansavefn(tag, int(default_for), ctx, self.bot.coc)

    @cog_ext.cog_slash(
        name="clan-clear",
        guild_ids=testguild,
        description="Clear a default clan that was previously saved",
        options=[
            create_option(
                name="default_of",
                description="Select which saved default to clear",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="Only mine", value="1"),
                    create_choice(name="This channel", value="3"),
                    create_choice(name="This category", value="3"),
                    create_choice(name="Entire server", value="4"),
                ],
            )
        ],
    )
    async def _clanclear(self, ctx: SlashContext, default_of: str):
        await ctx.defer()
        await clanclearfn(int(default_of), ctx)

    @cog_ext.cog_slash(
        name="clan-super",
        guild_ids=testguild,
        description="Find clan members with active super troops",
        options=[
            create_option(
                name="troop",
                description="Select the super troop from the list above",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="Super Barbarian", value="1"),
                    create_choice(name="Super Archer", value="2"),
                    create_choice(name="Super Giant", value="3"),
                    create_choice(name="Sneaky Goblin", value="4"),
                    create_choice(name="Super Wall Breaker", value="5"),
                    create_choice(name="Rocket Balloon", value="6"),
                    create_choice(name="Super Wizard", value="7"),
                    create_choice(name="Inferno Dragon", value="8"),
                    create_choice(name="Super Minion", value="9"),
                    create_choice(name="Super Valkyrie", value="10"),
                    create_choice(name="Super Witch", value="11"),
                    create_choice(name="Ice Hound", value="12"),
                    create_choice(name="Super Bowler", value="13"),
                    create_choice(name="Super Dragon", value="14"),
                    create_choice(name="Super Miner", value="15"),
                    create_choice(name="Super Hog Rider", value="16"),
                ],
            ),
            create_option(
                name="tag",
                description="Enter the clan tag with #",
                option_type=3,
                required=False,
            ),
        ],
    )
    async def _clansuper(self, ctx: SlashContext, troop: str, tag: str = ""):
        await ctx.defer()
        await clansuperfn(int(troop), tag, ctx, self.bot.coc)


def setup(bot):
    bot.add_cog(Clan(bot))
    print("Clan cog loaded!")
