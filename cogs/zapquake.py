from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from utility.zqprocess import zqprocess
from secret import testguild


class Zapquake(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="zapquake",
        description="ZapQuake combos for defenses and heroes",
        guild_ids=testguild,
        options=[
            create_option(
                name="defense",
                description="Select the defense from the list above",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="Archer Queen", value="1"),
                    create_choice(name="Barbarian King", value="2"),
                    create_choice(name="Royal Champion", value="3"),
                    create_choice(name="Grand Warden", value="4"),
                    create_choice(name="Eagle Artillery", value="5"),
                    create_choice(name="Scattershot", value="6"),
                    create_choice(name="Inferno Tower", value="7"),
                    create_choice(name="X-Bow", value="8"),
                    create_choice(name="Air Defense", value="9"),
                    create_choice(name="Air Sweeper", value="10"),
                    create_choice(name="Wizard Tower", value="11"),
                    create_choice(name="Hidden Tesla", value="12"),
                    create_choice(name="Builder's Hut", value="13"),
                    create_choice(name="Archer Tower", value="14"),
                    create_choice(name="Cannon", value="15"),
                    create_choice(name="Bomb Tower", value="16"),
                    create_choice(name="Mortar", value="17"),
                    create_choice(name="Spell Tower", value="18"),
                    create_choice(name="Monolith", value="19"),
                ],
            ),
            create_option(
                name="level",
                description="Enter the defense level and then click on zap above",
                option_type=4,
                required=True,
            ),
            create_option(
                name="zap",
                description="Select your lightning spell level from the list above",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="Level 10", value="10"),
                    create_choice(name="Level 9", value="9"),
                    create_choice(name="Level 8", value="8"),
                    create_choice(name="Level 7", value="7"),
                    create_choice(name="Level 6", value="6"),
                    create_choice(name="Level 5", value="5"),
                    create_choice(name="Level 4", value="4"),
                    create_choice(name="Level 3", value="3"),
                    create_choice(name="Level 2", value="2"),
                    create_choice(name="Level 1", value="1"),
                ],
            ),
            create_option(
                name="quake",
                description="Select your earthquake spell level from the list above",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="Level 5", value="5"),
                    create_choice(name="Level 4", value="4"),
                    create_choice(name="Level 3", value="3"),
                    create_choice(name="Level 2", value="2"),
                    create_choice(name="Level 1", value="1"),
                ],
            ),
            create_option(
                name="cc_space",
                description="Select your clan castle spell space from the list above",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="3 spell space", value="3"),
                    create_choice(name="2 spell space", value="2"),
                    create_choice(name="1 spell space", value="1"),
                    create_choice(name="0 spell space", value="0"),
                ],
            ),
            create_option(
                name="cc_zap",
                description="Select your clan castle lightning spell level from the list above",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="Level 10", value="10"),
                    create_choice(name="Level 9", value="9"),
                    create_choice(name="Level 8", value="8"),
                    create_choice(name="Level 7", value="7"),
                    create_choice(name="Level 6", value="6"),
                    create_choice(name="Level 5", value="5"),
                    create_choice(name="Level 4", value="4"),
                    create_choice(name="Level 3", value="3"),
                    create_choice(name="Level 2", value="2"),
                    create_choice(name="Level 1", value="1"),
                ],
            ),
            create_option(
                name="cc_quake",
                description="Select your clan castle earthquake spell level from the list above",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="Level 5", value="5"),
                    create_choice(name="Level 4", value="4"),
                    create_choice(name="Level 3", value="3"),
                    create_choice(name="Level 2", value="2"),
                    create_choice(name="Level 1", value="1"),
                ],
            ),
            create_option(
                name="warden",
                description="Enter enemy warden level (Only needed for heros under warden aura)",
                option_type=4,
                required=False,
            ),
        ],
    )
    async def _zqfind(
        self,
        ctx: SlashContext,
        defense: str,
        level: int,
        zap: str,
        quake: str,
        cc_space: str,
        cc_zap: str,
        cc_quake: str,
        warden: int = 0,
    ):
        await ctx.defer()
        await zqprocess(
            ctx,
            int(defense),
            level,
            int(zap),
            int(quake),
            int(cc_space),
            int(cc_zap),
            int(cc_quake),
            warden,
        )


def setup(bot):
    bot.add_cog(Zapquake(bot))
    print("ZapQuake cog loaded!")
