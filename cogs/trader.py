from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from utility.traderprocess import senditems, savedata, reminderloop
from secret import testguild


class Trader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminder.start()

    @tasks.loop(hours=1)
    async def reminder(self):
        await self.bot.wait_until_ready()
        await reminderloop(self.bot)

    @cog_ext.cog_slash(
        name="trader-next",
        guild_ids=testguild,
        description="Next occurance of an item in the Trader cycle",
        options=[
            create_option(
                name="item",
                description="Select a magic item from the list above",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="Book of Building", value="1"),
                    create_choice(name="Book of Fighting", value="2"),
                    create_choice(name="Book of Heroes", value="3"),
                    create_choice(name="Book of Spells", value="4"),
                    create_choice(name="Builder Potion", value="5"),
                    create_choice(name="Clock Tower Potion", value="6"),
                    create_choice(name="Hero Potion", value="7"),
                    create_choice(name="Power Potion", value="8"),
                    create_choice(name="Research Potion", value="9"),
                    create_choice(name="Resource Potion", value="10"),
                    create_choice(name="Super Potion", value="11"),
                    create_choice(name="Training Potion (Free)", value="12"),
                    create_choice(name="Training Potion (Gems)", value="13"),
                    create_choice(name="Wall Rings x5", value="14"),
                    create_choice(name="Wall Rings x10", value="15"),
                    create_choice(name="Shovel of Obstacles", value="16"),
                    create_choice(name="Rune of Builder Elixir", value="17"),
                    create_choice(name="Rune of Builder Gold", value="18"),
                    create_choice(name="Rune of Dark Elixir", value="19"),
                    create_choice(name="Rune of Elixir", value="20"),
                    create_choice(name="Rune of Gold", value="21"),
                ],
            ),
            create_option(
                name="reminder",
                description="Get a message the day this item appears next in your daily deals",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="On", value="1"),
                    create_choice(name="Off", value="0"),
                ],
            ),
        ],
    )
    async def _tradernext(self, ctx: SlashContext, item: str, reminder: str):
        if reminder == "1":
            rem = True
        else:
            rem = False
        await ctx.defer()
        await senditems(int(item), ctx, rem)

    @cog_ext.cog_slash(
        name="trader-save",
        guild_ids=testguild,
        description="Save or update your Trader cycle",
        options=[
            create_option(
                name="item1",
                description="Select your 1st magic item from the list above",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="Book of Building", value="1"),
                    create_choice(name="Book of Fighting", value="2"),
                    create_choice(name="Book of Heroes", value="3"),
                    create_choice(name="Book of Spells", value="4"),
                    create_choice(name="Builder Potion", value="5"),
                    create_choice(name="Clock Tower Potion", value="6"),
                    create_choice(name="Hero Potion", value="7"),
                    create_choice(name="Power Potion", value="8"),
                    create_choice(name="Research Potion", value="9"),
                    create_choice(name="Resource Potion", value="10"),
                    create_choice(name="Super Potion", value="11"),
                    create_choice(name="Training Potion (Free)", value="12"),
                    create_choice(name="Training Potion (Gems)", value="13"),
                    create_choice(name="Wall Rings x5", value="14"),
                    create_choice(name="Wall Rings x10", value="15"),
                    create_choice(name="Shovel of Obstacles", value="16"),
                    create_choice(name="Rune of Builder Elixir", value="17"),
                    create_choice(name="Rune of Builder Gold", value="18"),
                    create_choice(name="Rune of Dark Elixir", value="19"),
                    create_choice(name="Rune of Elixir", value="20"),
                    create_choice(name="Rune of Gold", value="21"),
                ],
            ),
            create_option(
                name="item2",
                description="Select your 2nd magic item from the list above",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="Book of Building", value="1"),
                    create_choice(name="Book of Fighting", value="2"),
                    create_choice(name="Book of Heroes", value="3"),
                    create_choice(name="Book of Spells", value="4"),
                    create_choice(name="Builder Potion", value="5"),
                    create_choice(name="Clock Tower Potion", value="6"),
                    create_choice(name="Hero Potion", value="7"),
                    create_choice(name="Power Potion", value="8"),
                    create_choice(name="Research Potion", value="9"),
                    create_choice(name="Resource Potion", value="10"),
                    create_choice(name="Super Potion", value="11"),
                    create_choice(name="Training Potion (Free)", value="12"),
                    create_choice(name="Training Potion (Gems)", value="13"),
                    create_choice(name="Wall Rings x5", value="14"),
                    create_choice(name="Wall Rings x10", value="15"),
                    create_choice(name="Shovel of Obstacles", value="16"),
                    create_choice(name="Rune of Builder Elixir", value="17"),
                    create_choice(name="Rune of Builder Gold", value="18"),
                    create_choice(name="Rune of Dark Elixir", value="19"),
                    create_choice(name="Rune of Elixir", value="20"),
                    create_choice(name="Rune of Gold", value="21"),
                ],
            ),
            create_option(
                name="item3",
                description="Select your 3rd magic item from the list above",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="Book of Building", value="1"),
                    create_choice(name="Book of Fighting", value="2"),
                    create_choice(name="Book of Heroes", value="3"),
                    create_choice(name="Book of Spells", value="4"),
                    create_choice(name="Builder Potion", value="5"),
                    create_choice(name="Clock Tower Potion", value="6"),
                    create_choice(name="Hero Potion", value="7"),
                    create_choice(name="Power Potion", value="8"),
                    create_choice(name="Research Potion", value="9"),
                    create_choice(name="Resource Potion", value="10"),
                    create_choice(name="Super Potion", value="11"),
                    create_choice(name="Training Potion (Free)", value="12"),
                    create_choice(name="Training Potion (Gems)", value="13"),
                    create_choice(name="Wall Rings x5", value="14"),
                    create_choice(name="Wall Rings x10", value="15"),
                    create_choice(name="Shovel of Obstacles", value="16"),
                    create_choice(name="Rune of Builder Elixir", value="17"),
                    create_choice(name="Rune of Builder Gold", value="18"),
                    create_choice(name="Rune of Dark Elixir", value="19"),
                    create_choice(name="Rune of Elixir", value="20"),
                    create_choice(name="Rune of Gold", value="21"),
                ],
            ),
        ],
    )
    async def _tradersave(self, ctx: SlashContext, item1: str, item2: str, item3: str):
        await ctx.defer()
        await savedata(int(item1), int(item2), int(item3), ctx)


def setup(bot):
    bot.add_cog(Trader(bot))
    print("Trader cog loaded!")
