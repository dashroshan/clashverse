from discord.ext import commands
from discord_slash import cog_ext
from secret import testguild
from discord import Embed as discord_Embed
from discord_slash.utils.manage_commands import create_option, create_choice
from re import compile, search
from discord_slash.utils.manage_components import create_actionrow, create_button
from math import ceil
from utility.errorimage import errorimg


class Servercmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_component(self, ctx):
        if (ctx.custom_id)[:4] == "role":
            roleid = int((ctx.custom_id)[4:])
            role = ctx.guild.get_role(roleid)
            if role == None:
                await ctx.send(
                    content="The role you're trying to get is no longer available in this server. Please ask a server admin to delete this embed message and create a new one with the available roles.",
                    hidden=True,
                )
                return
            try:
                if role in ctx.author.roles:
                    await ctx.author.remove_roles(role)
                    await ctx.send(
                        content=f"**{role.name}** role was removed for you!",
                        hidden=True,
                    )
                else:
                    await ctx.author.add_roles(role)
                    await ctx.send(
                        content=f"**{role.name}** role was added for you!", hidden=True
                    )
            except:
                await ctx.send(
                    f"**ClashVerse** role needs to have **Manage Roles** permission and should be present above the **{role.name}** role in the server settings inorder to add or remove that role for the users. Please point any server admin to this message."
                )

    async def rolebuttons(
        self,
        role_1,
        role_2,
        role_3,
        role_4,
        role_5,
        role_6,
        role_7,
        role_8,
        role_9,
        role_10,
    ):
        roles = []
        if role_1 != None and (role_1 not in roles):
            roles.append(role_1)
        if role_2 != None and (role_2 not in roles):
            roles.append(role_2)
        if role_3 != None and (role_3 not in roles):
            roles.append(role_3)
        if role_4 != None and (role_4 not in roles):
            roles.append(role_4)
        if role_5 != None and (role_5 not in roles):
            roles.append(role_5)
        if role_6 != None and (role_6 not in roles):
            roles.append(role_6)
        if role_7 != None and (role_7 not in roles):
            roles.append(role_7)
        if role_8 != None and (role_8 not in roles):
            roles.append(role_8)
        if role_9 != None and (role_9 not in roles):
            roles.append(role_9)
        if role_10 != None and (role_10 not in roles):
            roles.append(role_10)
        arows = []
        totalroles = len(roles)
        for i in range(ceil(len(roles) / 5)):
            roleset5 = roles[i * 5 : i * 5 + 5]
            arow = []
            for role in roleset5:
                btn = create_button(
                    label=role.name, style=2, custom_id=f"role{role.id}"
                )
                arow.append(btn)
            action_row = create_actionrow(*arow)
            arows.append(action_row)
        return arows, totalroles

    @cog_ext.cog_slash(
        name="embed",
        description="Create an embed with or without button roles",
        guild_ids=testguild,
        options=[
            create_option(
                name="heading",
                description="Enter heading (max 256 characters)",
                option_type=3,
                required=True,
            ),
            create_option(
                name="content",
                description="Enter main text content (max 4096 characters)",
                option_type=3,
                required=False,
            ),
            create_option(
                name="footer",
                description="Enter footer text (max 2048 characters)",
                option_type=3,
                required=False,
            ),
            create_option(
                name="colour",
                description="Enter hex value of sidebar colour (Google colour picker)",
                option_type=3,
                required=False,
            ),
            create_option(
                name="link",
                description="Enter link for the heading text",
                option_type=3,
                required=False,
            ),
            create_option(
                name="small_img",
                description="Enter link of small thumbnail image",
                option_type=3,
                required=False,
            ),
            create_option(
                name="large_img",
                description="Enter link of large bottom image",
                option_type=3,
                required=False,
            ),
            create_option(
                name="role_1",
                description="Select a role",
                option_type=8,
                required=False,
            ),
            create_option(
                name="role_2",
                description="Select a role",
                option_type=8,
                required=False,
            ),
            create_option(
                name="role_3",
                description="Select a role",
                option_type=8,
                required=False,
            ),
            create_option(
                name="role_4",
                description="Select a role",
                option_type=8,
                required=False,
            ),
            create_option(
                name="role_5",
                description="Select a role",
                option_type=8,
                required=False,
            ),
            create_option(
                name="role_6",
                description="Select a role",
                option_type=8,
                required=False,
            ),
            create_option(
                name="role_7",
                description="Select a role",
                option_type=8,
                required=False,
            ),
            create_option(
                name="role_8",
                description="Select a role",
                option_type=8,
                required=False,
            ),
            create_option(
                name="role_9",
                description="Select a role",
                option_type=8,
                required=False,
            ),
            create_option(
                name="role_10",
                description="Select a role",
                option_type=8,
                required=False,
            ),
        ],
    )
    async def _embedgen(
        self,
        ctx,
        heading,
        colour="#108adf",
        content="",
        small_img="",
        large_img="",
        link="",
        footer="",
        role_1=None,
        role_2=None,
        role_3=None,
        role_4=None,
        role_5=None,
        role_6=None,
        role_7=None,
        role_8=None,
        role_9=None,
        role_10=None,
    ):
        if ctx.author.guild_permissions.manage_messages == False:
            await errorimg(
                "You need Manage Messages permission to create an embed Chief!",
                1,
                ctx,
                True,
            )
            return
        if search(compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"), colour):
            colour = "0x" + colour[1:]
        else:
            await errorimg(
                "The hex value of colour appears invalid Chief! Google colour picker to get hex value of any colour you want",
                3,
                ctx,
                True,
            )
            return
        if (
            len(heading) > 255
            or len(content) > 4095
            or len(footer) > 2047
            or (
                len(heading)
                + len(content)
                + len(footer)
                + len(colour)
                + len(link)
                + len(small_img)
                + len(large_img)
            )
            > 5800
        ):
            await errorimg(
                "You exceeded the maximum character limit of some fields Chief!",
                1,
                ctx,
                True,
            )
            return

        embed = discord_Embed(
            title=heading, color=eval(colour), description=content, url=link
        )
        if footer != "":
            embed.set_footer(text=footer)
        if large_img != "":
            embed.set_image(url=large_img)
        if small_img != "":
            embed.set_thumbnail(url=small_img)

        action_row, totalroles = await self.rolebuttons(
            role_1,
            role_2,
            role_3,
            role_4,
            role_5,
            role_6,
            role_7,
            role_8,
            role_9,
            role_10,
        )

        if totalroles != 0 and ctx.author.guild_permissions.manage_roles == False:
            await errorimg(
                "You need Manage Roles permission for adding button roles Chief!",
                1,
                ctx,
                True,
            )
            return

        await ctx.channel.send(embed=embed, components=action_row)
        if totalroles != 0:
            await ctx.send(
                content="For the proper functioning of the button roles, please ensure that the **ClashVerse** role has **Manage Roles** permission and is present above the role(s) it is to handle in the server settings.",
                hidden=True,
            )
        else:
            await ctx.send(content="Embed created successfully!", hidden=True)


def setup(bot):
    bot.add_cog(Servercmd(bot))
    print("Server cog loaded!")
