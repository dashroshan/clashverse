# Private tracking of war attack and war cc donation misses for mightysword
from discord.ext import commands
import pymongo
from datetime import datetime, timedelta
from secret import mongodb_url, swordchannel
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

db_client = pymongo.MongoClient(mongodb_url)
db = db_client.mightytracker
collection = db.sword
warcccol = db.warcc


class Swordtracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def dbupdateone(self, tag):
        record = collection.find_one({"tag": tag})
        misscount = record["misscount"]
        dayspassed = (datetime.utcnow() - record["lastchange"]).days
        missreduce = dayspassed // 30
        if (misscount - missreduce) <= 0:
            collection.delete_many({"tag": tag})
        else:
            misscount -= missreduce
            misses = record["misses"]
            if missreduce == 1:
                misses.pop(0)
                daysleft = dayspassed % 30
                lastchange = datetime.utcnow() - timedelta(days=daysleft)
                collection.update_one(
                    {"tag": tag},
                    {
                        "$set": {
                            "misscount": misscount,
                            "misses": misses,
                            "lastchange": lastchange,
                        }
                    },
                )

    async def dbupdateall(self):
        for i in collection.find({}):
            tag = i["tag"]
            await self.dbupdateone(tag)

    async def dbclear(self, tag):  # tag includes hash
        count = collection.delete_many({"tag": tag}).deleted_count
        if count == 0:
            msg = f"{tag} not found in the record of war misses!"
        else:
            msg = f"All war miss records for {tag} has been cleared!"
        return msg

    async def dbmiss(self, tag):
        count = collection.count_documents({"tag": tag})
        if count == 0:
            try:
                player = await self.bot.coc.get_player(tag)
                pname = str(player.name)
            except Exception as error:
                print(error)
                msg = "No player found with the given tag!"
                return msg
            record = {
                "name": pname,
                "tag": tag,
                "misscount": 1,
                "misses": [datetime.utcnow()],
                "lastchange": datetime.utcnow(),
            }
            collection.insert_one(record)
            msg = f"Record for **{record['name']}({tag})** updated!\n**Attacks missed:** 1\n**Action to take:** No actions required, or inform him/her not to miss war attacks in the future."
        else:
            await self.dbupdateone(tag)
            record = collection.find_one({"tag": tag})
            misscount = record["misscount"]
            misses = record["misses"]
            if misscount == 1:
                misses.append(datetime.utcnow())
                collection.update_one(
                    {"tag": tag},
                    {
                        "$set": {
                            "misscount": 2,
                            "misses": misses,
                            "lastchange": datetime.utcnow(),
                        }
                    },
                )
                msg = f"Record for **{record['name']}({tag})** updated!\n**Attacks missed:** 2\n**Action to take:** Issue final warning that s/he will be kicked or demoted if misses another attack within a month."
            elif misscount == 2:
                collection.delete_many({"tag": tag})
                msg = f"Record for **{record['name']}({tag})** updated!\n**Attacks missed:** 3\n**Action to take:** Kick or demote"
        return msg

    async def dbinfoone(self, tag):
        count = collection.count_documents({"tag": tag})
        if count == 0:
            msg = "No war miss records found for the given player!"
            return msg
        await self.dbupdateone(tag)
        record = collection.find_one({"tag": tag})
        misscount = record["misscount"]
        msg = (
            "**Name: **"
            + record["name"]
            + "\n**Attacks missed: **"
            + str(record["misscount"])
            + "\n**1st miss: **"
            + str(record["misses"][0].date())
        )
        if misscount == 2:
            msg += "\n**2nd miss: **" + str(record["misses"][1].date())
        return msg

    async def dbinfoall(self):
        await self.dbupdateall()
        msg = "**`" + "Name".ljust(15, " ") + "   1st miss      2nd miss" + "`**\n"
        msg += "**Missed two war attacks:**\n"
        counttwo = collection.count_documents({"misscount": 2})
        countone = collection.count_documents({"misscount": 1})
        if counttwo == 0:
            msg += "`" + "None".ljust(40, " ") + "`\n"
        for i in collection.find({"misscount": 2}):
            msg += (
                "`"
                + i["name"].ljust(15, " ")
                + " "
                + str(i["misses"][0].date())
                + "    "
                + str(i["misses"][1].date())
                + "`\n"
            )
        msg += "**Missed one war attack:**\n"
        if countone == 0:
            msg += "`" + "None".ljust(40, " ") + "`\n"
        for j in collection.find({"misscount": 1}):
            msg += (
                "`"
                + j["name"].ljust(15, " ")
                + " "
                + str(j["misses"][0].date())
                + "              `\n"
            )
        return msg

    async def dbccmiss(self, tag):
        count = warcccol.count_documents({"tag": tag})
        if count == 0:
            try:
                player = await self.bot.coc.get_player(tag)
                pname = str(player.name)
            except Exception as error:
                print(error)
                return False
            record = {"name": pname, "tag": tag, "misses": [datetime.utcnow()]}
            warcccol.insert_one(record)
        else:
            record = warcccol.find_one({"tag": tag})
            misses = record["misses"]
            misses.insert(0, datetime.utcnow())
            warcccol.update_one({"tag": tag}, {"$set": {"misses": misses}})
        return True

    async def dbccinfo(self):
        msg = ""
        for i in warcccol.find({}):
            msg += i["name"] + " : `"
            for j in i["misses"]:
                msg += str(j.date()) + ", "
            msg = msg[:-2]
            msg += "`\n"
        return msg

    @cog_ext.cog_slash(
        name="sword-miss",
        description="Save war miss record of a member",
        guild_ids=[401447829395996692],
        options=[
            create_option(
                name="tag",
                description="Enter the player tag with #",
                option_type=3,
                required=True,
            )
        ],
    )
    async def miss(self, ctx, tag: str):
        await ctx.defer()
        if ctx.channel.id == swordchannel:
            if tag[0] == "#":
                tosend = await self.dbmiss(tag)
            else:
                tosend = "Invalid tag!"
            await ctx.send(tosend)
        else:
            await ctx.send(content="This is a sword leaders only command!", hidden=True)

    @cog_ext.cog_slash(
        name="sword-info",
        description="Get all war miss records",
        guild_ids=[401447829395996692],
    )
    async def info(self, ctx):
        await ctx.defer()
        if ctx.channel.id == swordchannel:
            tosend = await self.dbinfoall()
            await ctx.send(tosend)
        else:
            await ctx.send(content="This is a sword leaders only command!", hidden=True)

    @cog_ext.cog_slash(
        name="sword-clear",
        description="Clear war miss records of a member",
        guild_ids=[401447829395996692],
        options=[
            create_option(
                name="tag",
                description="Enter the player tag with #",
                option_type=3,
                required=True,
            )
        ],
    )
    async def clear(self, ctx, tag: str):
        await ctx.defer()
        if ctx.channel.id == swordchannel:
            if tag[0] == "#":
                tosend = await self.dbclear(tag)
            else:
                tosend = "Invalid tag!"
            await ctx.send(tosend)
        else:
            await ctx.send(content="This is a sword leaders only command!", hidden=True)


def setup(bot):
    bot.add_cog(Swordtracker(bot))
    print("Swordtracker cog loaded!")
