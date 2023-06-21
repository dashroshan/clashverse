# import dns.resolver
# dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
# dns.resolver.default_resolver.nameservers=['8.8.8.8'] # remove this, only for mobile

from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from discord import File as discord_File
import pymongo
from secret import mongodb_url
from utility.errorimage import errorimg

db_client = pymongo.MongoClient(mongodb_url)
db = db_client.discordbot
collection = db.userdata

cycledays = {
    1: [15, 9, 5],
    2: [11, 7, 20],
    3: [6, 14, 5],
    4: [11, 7, 18],
    5: [12, 7, 4],
    6: [13, 9, 3],
    7: [11, 9, 19],
    8: [13, 14, 5],
    9: [15, 16, 5],
    10: [11, 7, 21],
    11: [11, 10, 4],
    12: [13, 14, 2],
    13: [12, 9, 5],
    14: [13, 8, 1],
    15: [14, 9, 3],
    16: [13, 8, 5],
    17: [15, 10, 20],
    18: [13, 9, 5],
    19: [6, 10, 2],
    20: [12, 10, 3],
    21: [13, 8, 21],
    22: [13, 9, 5],
    23: [13, 14, 4],
    24: [13, 9, 5],
    25: [11, 16, 1],
    26: [6, 9, 1],
    27: [11, 8, 5],
    28: [13, 7, 1],
    29: [13, 10, 21],
    30: [13, 9, 5],
    31: [12, 8, 5],
    32: [13, 9, 5],
    33: [15, 8, 3],
    34: [13, 7, 5],
    35: [13, 14, 21],
    36: [14, 8, 5],
    37: [6, 10, 2],
    38: [12, 10, 5],
    39: [17, 10, 5],
}


async def reminderimg(day, text, ctx):
    font = ImageFont.truetype("utility/assets/thick.ttf", 20)
    img = Image.open("utility/assets/trader/panel.png")
    items = Image.open(f"utility/assets/trader/{day}.png")
    draw = ImageDraw.Draw(img)
    draw.text(
        (300, 40),
        text,
        fill=(0, 0, 0),
        font=font,
        stroke_width=2,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )
    draw.text(
        (300, 37),
        text,
        fill=(255, 255, 255),
        font=font,
        stroke_width=2,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )
    img.paste(items, (47, 80), items)
    with BytesIO() as image:
        img = img.convert("P", palette=Image.ADAPTIVE)
        img.save(image, "PNG")
        image.seek(0)
        await ctx.send(file=discord_File(fp=image, filename=f"trader_day{day}.png"))


async def reminderloop(disbot):
    date = datetime.utcnow()
    count = collection.count_documents(
        {"type": "reminder", "day": int(date.day), "month": int(date.strftime("%m"))}
    )
    if count == 0:
        return
    for data in collection.find(
            {"type": "reminder", "day": int(date.day), "month": int(date.strftime("%m"))}
    ):
        try:
            user = disbot.get_user(data["user"])
            await reminderimg(data["tday"], "Reminder : Trader items today", user)
        except:
            pass
    collection.delete_many(
        {"type": "reminder", "day": int(date.day), "month": int(date.strftime("%m"))}
    )


async def itemimage(day, text, ctx, date, reminder):
    font = ImageFont.truetype("utility/assets/thick.ttf", 20)
    img = Image.open("utility/assets/trader/panel.png")
    items = Image.open(f"utility/assets/trader/{day}.png")
    draw = ImageDraw.Draw(img)
    draw.text(
        (300, 40),
        text,
        fill=(0, 0, 0),
        font=font,
        stroke_width=2,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )
    draw.text(
        (300, 37),
        text,
        fill=(255, 255, 255),
        font=font,
        stroke_width=2,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )
    img.paste(items, (47, 80), items)
    with BytesIO() as image:
        img = img.convert("P", palette=Image.ADAPTIVE)
        img.save(image, "PNG")
        image.seek(0)
        await ctx.send(file=discord_File(fp=image, filename=f"trader_day{day}.png"))

    if reminder == True:
        count = collection.count_documents(
            {
                "type": "reminder",
                "day": int(date.day),
                "month": int(date.strftime("%m")),
                "user": ctx.author.id,
            }
        )
        if count != 0:
            await ctx.send(
                content="You have a reminder saved for this day previously!",
                hidden=True,
            )
            return
        data = {
            "type": "reminder",
            "day": int(date.day),
            "month": int(date.strftime("%m")),
            "tday": day,
            "user": ctx.author.id,
        }
        collection.insert_one(data)
        await ctx.send(content="Reminder saved!", hidden=True)


async def finditems(datetimeobj, day, itemid, ctx, reminder):
    days = datetime.utcnow().day - datetimeobj.day
    today = (days + day) % 39
    before, after = [], []
    for date, item in cycledays.items():
        if itemid in item:
            if date < today:
                before.append(date)
            elif date > today:
                after.append(date)
    if len(after) != 0:
        allitems = after[0]
        nextdate = datetime.utcnow() + timedelta(days=after[0] - today)
    elif len(before) != 0:
        allitems = before[0]
        nextdate = datetime.utcnow() + timedelta(days=39 + before[0] - today)
    else:
        allitems = today
        nextdate = datetime.utcnow()
    date = nextdate.strftime("%d")
    month = nextdate.strftime("%B")
    day = nextdate.strftime("%A")
    nextdate2 = f"{date} {month} : {day}"
    await itemimage(allitems, nextdate2, ctx, nextdate, reminder)


async def senditems(item, ctx, reminder):
    count = collection.count_documents({"id": ctx.author.id})
    if count == 0:
        await errorimg(
            "You need to save your\ntrader cycle before\nyou can use this Chief!\n\nUse /trader-save",
            1,
            ctx,
            False,
        )
        return
    record = collection.find_one({"id": ctx.author.id})
    await finditems(record["tradersavedate"], record["traderday"], item, ctx, reminder)


async def savedata(item1, item2, item3, ctx):
    items = [item1, item2, item3]
    for date, item in cycledays.items():
        if item == items:
            if date == 19 or date == 37:
                await errorimg(
                    "This item combo is available on two different days Chief! Save your trader cycle tomorrow instead",
                    1,
                    ctx,
                    True,
                )
                return
            data = {
                "id": ctx.author.id,
                "traderday": date,
                "tradersavedate": datetime.utcnow(),
            }
            count = collection.count_documents({"id": ctx.author.id})
            if count == 0:
                collection.insert_one(data)
                await errorimg(
                    "The trader cycle has\nbeen saved Chief! You\ncan now find the next\noccurance of any item\nusing /trader-next",
                    2,
                    ctx,
                    False,
                )
                return
            else:
                collection.update_one(
                    {"id": ctx.author.id},
                    {"$set": {"traderday": date, "tradersavedate": datetime.utcnow()}},
                )
                await errorimg(
                    "The trader cycle has\nbeen updated Chief! You\ncan now find the next\noccurance of any item\nusing /trader-next",
                    2,
                    ctx,
                    False,
                )
                return
    await errorimg(
        "The items combination\ndoesn't appear to be\nvalid Chief! Can you\ncheck it again in-game\nand retry?",
        3,
        ctx,
        False,
    )
