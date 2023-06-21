from discord import File as discord_File
import pymongo
from secret import mongodb_url
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from utility.errorimage import errorimg
from math import ceil
from requests import get as requests_get
from coc.errors import PrivateWarLog
from datetime import datetime, timedelta
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle

db_client = pymongo.MongoClient(mongodb_url)
db = db_client.discordbot
collection = db.clandata


async def getsavedtag(ctx):
    if ctx.channel == None:
        await errorimg(
            "Discord threads aren't completely supported by ClashVerse yet",
            1,
            ctx,
            True,
        )
        return False
    data = collection.find_one({"channel": ctx.channel.id})
    if data != None:
        return data["tag"]
    if ctx.channel.category != None:
        data = collection.find_one({"category": ctx.channel.category.id})
        if data != None:
            return data["tag"]
    data = collection.find_one({"server": ctx.guild.id})
    if data != None:
        return data["tag"]
    data = collection.find_one({"user": ctx.author.id})
    if data != None:
        return data["tag"]
    await errorimg(
        "You need to save your clan using /clan-save or use the tag option of this command Chief!",
        1,
        ctx,
        True,
    )
    return False


async def clanclearfn(default_of, ctx):
    if ctx.channel == None:
        await errorimg(
            "Discord threads aren't completely supported by ClashVerse yet",
            1,
            ctx,
            True,
        )
        return
    if default_of > 1 and ctx.author.guild_permissions.manage_channels == False:
        await errorimg(
            "You need manage channels permission to clear the clan saved for this channel Chief!",
            1,
            ctx,
            True,
        )
        return

    if default_of == 1:
        dfor, did, dmsg = "user", ctx.author.id, "you"
    elif default_of == 2:
        dfor, did, dmsg = "channel", ctx.channel.id, "this channel"
    elif default_of == 3:
        if ctx.channel.category == None:
            await errorimg("This is an uncategorized channel Chief!", 1, ctx, True)
            return
        dfor, did, dmsg = "category", ctx.channel.category.id, "this category"
    elif default_of == 4:
        dfor, did, dmsg = "server", ctx.guild.id, "this server"

    count = collection.count_documents({dfor: did})
    if count == 0:
        await errorimg(
            f"There wasn't any clan saved for {dmsg} to clear Chief!", 1, ctx, True
        )
        return
    collection.delete_many({dfor: did})
    await errorimg(f"The clan saved for {dmsg} was cleared Chief!", 2, ctx, True)


async def clansavefn(tag, default_for, ctx, cocc):
    if ctx.channel == None:
        await errorimg(
            "Discord threads aren't completely supported by ClashVerse yet",
            1,
            ctx,
            True,
        )
        return
    if default_for > 1 and ctx.author.guild_permissions.manage_channels == False:
        await errorimg(
            "You need manage channels permission to save a clan for this channel Chief!",
            1,
            ctx,
            True,
        )
        return

    if default_for == 1:
        dfor, did, dmsg = "user", ctx.author.id, "you"
    elif default_for == 2:
        dfor, did, dmsg = "channel", ctx.channel.id, "this channel"
    elif default_for == 3:
        if ctx.channel.category == None:
            await errorimg("This is an uncategorized channel Chief!", 1, ctx, True)
            return
        dfor, did, dmsg = "category", ctx.channel.category.id, "this category"
    elif default_for == 4:
        dfor, did, dmsg = "server", ctx.guild.id, "this server"

    try:
        clan = await cocc.get_clan(tag)
    except:
        await errorimg(
            "The tag seems to be invalid Chief! Can you copy it again from the game and retry?",
            3,
            ctx,
            True,
        )
        return

    data = {dfor: did, "tag": tag}
    count = collection.count_documents({dfor: did})
    if count == 0:
        collection.insert_one(data)
        await errorimg(
            f"{clan.name} has been saved as the default clan for {dmsg} Chief!",
            2,
            ctx,
            True,
        )
        return
    else:
        collection.update_one({"id": ctx.author.id}, {"$set": {"tag": tag}})
        await errorimg(
            f"{clan.name} has been saved as the new default clan for {dmsg} Chief!",
            2,
            ctx,
            True,
        )
        return


async def clanwar_lineupfn(ctx, tag, cocc):
    if tag == "":
        tag = await getsavedtag(ctx)
        if tag == False:
            return
    try:
        war = await cocc.get_current_war(tag)
    except PrivateWarLog:
        await errorimg(
            "The war log seems to be private Chief! It needs to be public for using this command.",
            1,
            ctx,
            True,
        )
        return
    except:
        await errorimg(
            "The tag seems to be invalid Chief! Can you copy it again from the game and retry?",
            3,
            ctx,
            True,
        )
        return
    if war == None:
        await errorimg(
            f"The clan is currently inaccessible Chief! Please try again after sometime.",
            4,
            ctx,
            True,
        )
        return
    if war.is_cwl == False:
        if war.state.lower() not in ["preparation", "inwar"]:
            await errorimg(f"Clan is not at war right now Chief!", 1, ctx, True)
            return
    ownptags = [p.tag for p in war.clan.members]
    enemyptags = [p.tag for p in war.opponent.members]
    ownp, enemyp = [], []
    nontroops = [
        "L.A.S.S.I",
        "Electro Owl",
        "Mighty Yak",
        "Unicorn",
        "Wall Wrecker",
        "Battle Blimp",
        "Stone Slammer",
        "Siege Barracks",
        "Log Launcher",
        "Super Barbarian",
        "Super Archer",
        "Super Giant",
        "Sneaky Goblin",
        "Super Wall Breaker",
        "Super Wizard",
        "Inferno Dragon",
        "Super Minion",
        "Super Valkyrie",
        "Super Witch",
        "Ice Hound",
        "Super Bowler",
        "Rocket Balloon",
    ]
    async for member in cocc.get_players(ownptags + enemyptags):
        herosum, petsum, spellsum, troopsum = 0, 0, 0, 0
        for hero in member.heroes:
            if hero.is_home_base:
                herosum += hero.level / hero.max_level
        for pet in member.pets:
            petsum += pet.level
        for spell in member.spells:
            spellsum += spell.level / spell.max_level
        for troop in member.home_troops:
            if troop.name not in nontroops:
                troopsum += troop.level / troop.max_level
        tspercent = ceil(((spellsum + troopsum) / 36) * 100)
        heropercent = ceil(((herosum + (petsum / 40)) / 5) * 100)
        data = [f"Th{member.town_hall}", f"{heropercent}%", f"{tspercent}%"]
        if member.tag in ownptags:
            ownp.append(data)
        else:
            enemyp.append(data)
    printdata = [i + j for i, j in zip(ownp, enemyp)]
    # ownclanname=war.clan.name
    # enemyclanname=war.opponent.name
    intname1 = war.clan.name.encode("ascii", "ignore").decode()
    intname2 = war.opponent.name.encode("ascii", "ignore").decode()
    if intname1 == "":
        ownclanname = war.clan.tag
    else:
        ownclanname = intname1
    if intname2 == "":
        enemyclanname = war.opponent.tag
    else:
        enemyclanname = intname2
    titlefont = ImageFont.truetype("utility/assets/thick.ttf", 18)
    thickfont = ImageFont.truetype("utility/assets/thick.ttf", 14)
    thinfont = ImageFont.truetype("utility/assets/thin.ttf", 15)
    labelimg = Image.open("utility/assets/war/dataimg.png")
    labelmimg = Image.open("utility/assets/war/dataimgmask.png")
    labelcimg = Image.open("utility/assets/war/clanslabel.png")
    printdata = [
        printdata[i * 5 : (i + 1) * 5] for i in range((len(printdata) + 5 - 1) // 5)
    ]
    firstsubdata = True
    posid = 0
    imgid = 1
    files = []
    for subdata in printdata:
        if len(subdata) == 10:
            bgimg = Image.open("utility/assets/war/bg10.png")
        else:
            bgimg = Image.open("utility/assets/war/bg5.png")
        yco = -30
        for data in subdata:
            yco += 40
            posid += 1
            limgtemp = labelimg.copy()
            draw = ImageDraw.Draw(limgtemp)
            draw.text(
                (289, 23),
                str(posid),
                fill=(0, 0, 0),
                font=thickfont,
                stroke_width=1,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )
            draw.text(
                (289, 20),
                str(posid),
                fill=(255, 255, 255),
                font=thickfont,
                stroke_width=1,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )
            draw.text(
                (319, 23),
                data[3],
                fill=(0, 0, 0),
                font=thickfont,
                stroke_width=1,
                stroke_fill=(0, 0, 0),
                anchor="lm",
            )
            draw.text(
                (319, 21),
                data[3],
                fill=(255, 255, 255),
                font=thickfont,
                stroke_width=1,
                stroke_fill=(0, 0, 0),
                anchor="lm",
            )
            draw.text(
                (421, 20),
                data[4],
                fill=(255, 255, 255),
                font=thinfont,
                stroke_width=1,
                stroke_fill=(0, 0, 0),
                anchor="lm",
            )
            draw.text(
                (513, 20),
                data[5],
                fill=(255, 255, 255),
                font=thinfont,
                stroke_width=1,
                stroke_fill=(0, 0, 0),
                anchor="lm",
            )
            draw.text(
                (257, 23),
                data[0],
                fill=(0, 0, 0),
                font=thickfont,
                stroke_width=1,
                stroke_fill=(0, 0, 0),
                anchor="rm",
            )
            draw.text(
                (257, 21),
                data[0],
                fill=(255, 255, 255),
                font=thickfont,
                stroke_width=1,
                stroke_fill=(0, 0, 0),
                anchor="rm",
            )
            draw.text(
                (62, 20),
                data[2],
                fill=(255, 255, 255),
                font=thinfont,
                stroke_width=1,
                stroke_fill=(0, 0, 0),
                anchor="rm",
            )
            draw.text(
                (152, 20),
                data[1],
                fill=(255, 255, 255),
                font=thinfont,
                stroke_width=1,
                stroke_fill=(0, 0, 0),
                anchor="rm",
            )
            bgimg.paste(limgtemp, (12, yco), labelmimg)

        if firstsubdata == True:
            firstsubdata = False
            if len(subdata) == 10:
                imght = 476
            else:
                imght = 277
            firstimg = Image.new("RGBA", (600, imght), color=(225, 225, 225, 0))
            firstimg.paste(bgimg, (0, 55), bgimg)
            firstimg.paste(labelcimg, (0, 0), labelcimg)
            draw = ImageDraw.Draw(firstimg)
            draw.text(
                (260, 31),
                ownclanname,
                fill=(0, 0, 0),
                font=titlefont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="rm",
            )
            draw.text(
                (260, 29),
                ownclanname,
                fill=(255, 255, 255),
                font=titlefont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="rm",
            )
            draw.text(
                (300, 31),
                "VS",
                fill=(0, 0, 0),
                font=titlefont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )
            draw.text(
                (300, 29),
                "VS",
                fill=(255, 255, 255),
                font=titlefont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )
            draw.text(
                (340, 31),
                enemyclanname,
                fill=(0, 0, 0),
                font=titlefont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="lm",
            )
            draw.text(
                (340, 29),
                enemyclanname,
                fill=(255, 255, 255),
                font=titlefont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="lm",
            )
            bgimg = firstimg

        with BytesIO() as image:
            bgimg = bgimg.convert("P", palette=Image.ADAPTIVE)
            bgimg.save(image, "PNG")
            image.seek(0)
            files.append(discord_File(fp=image, filename=f"lineup{imgid}.png"))
            imgid += 1
    await ctx.send(files=files)


async def clanwar_scoreboardfn(ctx, tag, cocc):
    if tag == "":
        tag = await getsavedtag(ctx)
        if tag == False:
            return
    try:
        war = await cocc.get_current_war(tag)
    except PrivateWarLog:
        await errorimg(
            "The war log seems to be private Chief! It needs to be public for using this command.",
            1,
            ctx,
            True,
        )
        return
    except:
        await errorimg(
            "The tag seems to be invalid Chief! Can you copy it again from the game and retry?",
            3,
            ctx,
            True,
        )
        return
    wdata = {}
    if war == None:
        await errorimg(
            f"The clan is currently inaccessible Chief! Please try again after sometime.",
            4,
            ctx,
            True,
        )
        return
    if war.is_cwl == False:
        if war.state.lower() not in ["preparation", "inwar"]:
            await errorimg(f"Clan is not at war right now Chief!", 1, ctx, True)
            return
    nofattack = 2
    endt = war.end_time.time - datetime.utcnow()
    if war.is_cwl == True:
        nofattack = 1
    if endt.days == 0:
        wtext = "Battle day - "
        def1, def2 = {}, {}
        for attack in war.attacks:
            if (
                attack.attacker.is_opponent == False
                and def2.get(attack.defender_tag, 0) <= attack.stars
            ):
                def2[attack.defender_tag] = attack.stars
            elif (
                attack.attacker.is_opponent == True
                and def1.get(attack.defender_tag, 0) <= attack.stars
            ):
                def1[attack.defender_tag] = attack.stars
            star1, star2 = {0: 0, 1: 0, 2: 0, 3: 0}, {0: 0, 1: 0, 2: 0, 3: 0}
            for i in def1:
                star1[def1[i]] += 1
            for i in def2:
                star2[def2[i]] += 1
            wdata["stars2"] = (
                str(star1[3]).zfill(2)
                + "\n"
                + str(star1[2]).zfill(2)
                + "\n"
                + str(star1[1]).zfill(2)
                + "\n"
                + str(star1[0]).zfill(2)
            )
            wdata["stars1"] = (
                str(star2[3]).zfill(2)
                + "\n"
                + str(star2[2]).zfill(2)
                + "\n"
                + str(star2[1]).zfill(2)
                + "\n"
                + str(star2[0]).zfill(2)
            )
    elif endt.days < 0:
        await errorimg(f"Clan is not at war right now Chief!", 1, ctx, True)
        return
    else:
        endt = war.start_time.time - datetime.utcnow()
        wtext = "Preparation day - "
        wdata["stars1"] = "00\n00\n00\n00"
        wdata["stars2"] = "00\n00\n00\n00"
    endh = endt.seconds // 3600
    endm = (endt.seconds // 60) % 60
    wdata["state"] = wtext + f"{endh}h {endm}m left"
    wdata["badge1"], wdata["badge2"] = war.clan.badge.small, war.opponent.badge.small
    wdata["name1"], wdata["name2"] = war.clan.name, war.opponent.name
    wdata["star"] = (
        str(war.clan.stars).zfill(2) + " - " + str(war.opponent.stars).zfill(2)
    )
    wdata["attack1"], wdata["attack2"] = str(war.clan.attacks_used) + "/" + str(
        war.team_size * nofattack
    ), str(war.opponent.attacks_used) + "/" + str(war.team_size * nofattack)
    wdata["dest1"], wdata["dest2"] = (
        f"{'%.2f' % war.clan.destruction}%",
        f"{'%.2f' % war.opponent.destruction}%",
    )
    wardata = wdata

    img = Image.open("utility/assets/war/scoreboard.png")
    draw = ImageDraw.Draw(img)
    thickfont = ImageFont.truetype("utility/assets/thick.ttf", 16)
    thinfont = ImageFont.truetype("utility/assets/thin.ttf", 17)

    badge1 = Image.open(BytesIO(requests_get(wardata["badge1"]).content)).resize(
        (48, 48)
    )
    badge2 = Image.open(BytesIO(requests_get(wardata["badge2"]).content)).resize(
        (48, 48)
    )
    img.paste(badge2, (300, 10), badge2)
    img.paste(badge1, (252, 10), badge1)

    draw.text(
        (229, 73),
        wardata["attack1"],
        fill=(255, 255, 255),
        font=thinfont,
        stroke_width=1,
        stroke_fill=(0, 0, 0),
        anchor="rm",
    )

    draw.text(
        (371, 73),
        wardata["attack2"],
        fill=(255, 255, 255),
        font=thinfont,
        stroke_width=1,
        stroke_fill=(0, 0, 0),
        anchor="lm",
    )

    intname1 = wardata["name1"].encode("ascii", "ignore").decode()
    intname2 = wardata["name2"].encode("ascii", "ignore").decode()
    if intname1 == "":
        wardata["name1"] = war.clan.tag
    else:
        wardata["name1"] = intname1
    if intname2 == "":
        wardata["name2"] = war.opponent.tag
    else:
        wardata["name2"] = intname2

    draw.text(
        (249, 53),
        wardata["name1"],
        fill=(0, 0, 0),
        font=thickfont,
        stroke_width=1,
        stroke_fill=(0, 0, 0),
        anchor="rm",
    )
    draw.text(
        (249, 51),
        wardata["name1"],
        fill=(255, 255, 255),
        font=thickfont,
        stroke_width=1,
        stroke_fill=(0, 0, 0),
        anchor="rm",
    )

    draw.text(
        (351, 53),
        wardata["name2"],
        fill=(0, 0, 0),
        font=thickfont,
        stroke_width=1,
        stroke_fill=(0, 0, 0),
        anchor="lm",
    )
    draw.text(
        (351, 51),
        wardata["name2"],
        fill=(255, 255, 255),
        font=thickfont,
        stroke_width=1,
        stroke_fill=(0, 0, 0),
        anchor="lm",
    )

    draw.text(
        (299, 71),
        wardata["star"],
        fill=(0, 0, 0),
        font=thickfont,
        stroke_width=1,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )
    draw.text(
        (299, 69),
        wardata["star"],
        fill=(255, 255, 255),
        font=thickfont,
        stroke_width=1,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )

    draw.text(
        (300, 141),
        wardata["state"],
        fill=(0, 0, 0),
        font=thickfont,
        stroke_width=1,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )
    draw.text(
        (300, 139),
        wardata["state"],
        fill=(255, 255, 255),
        font=thickfont,
        stroke_width=1,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )

    draw.text(
        (135, 103),
        wardata["dest1"],
        fill=(255, 255, 255),
        font=thinfont,
        stroke_width=1,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )

    draw.text(
        (467, 103),
        wardata["dest2"],
        fill=(255, 255, 255),
        font=thinfont,
        stroke_width=1,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )

    draw.text(
        (131, 232),
        wardata["stars1"],
        fill=(0, 0, 0),
        font=thickfont,
        stroke_width=2,
        stroke_fill=(0, 0, 0),
        align="center",
        anchor="mm",
        spacing=17,
    )
    draw.text(
        (131, 230),
        wardata["stars1"],
        fill=(255, 255, 255),
        font=thickfont,
        stroke_width=2,
        stroke_fill=(0, 0, 0),
        anchor="mm",
        align="center",
        spacing=17,
    )

    draw.text(
        (467, 232),
        wardata["stars2"],
        fill=(0, 0, 0),
        font=thickfont,
        stroke_width=2,
        stroke_fill=(0, 0, 0),
        align="center",
        anchor="mm",
        spacing=17,
    )
    draw.text(
        (467, 230),
        wardata["stars2"],
        fill=(255, 255, 255),
        font=thickfont,
        stroke_width=2,
        stroke_fill=(0, 0, 0),
        anchor="mm",
        align="center",
        spacing=17,
    )

    with BytesIO() as image:
        img = img.convert("P", palette=Image.ADAPTIVE)
        img.save(image, "PNG")
        image.seek(0)
        await ctx.send(
            file=discord_File(fp=image, filename=f"scoreboard.png"),
            components=[
                create_actionrow(
                    create_button(
                        style=ButtonStyle.URL,
                        label="Enemy War Log",
                        url=f"https://cocp.it/clan/{(war.opponent.tag)[1:]}",
                    )
                )
            ],
        )


maxherolvl = {
    "15": ["90", "90", "65", "40"],
    "14": ["80", "80", "55", "30"],
    "13": ["75", "75", "50", "25"],
    "12": ["65", "65", "40", "0"],
    "11": ["50", "50", "20", "0"],
    "10": ["40", "40", "0", "0"],
    "9": ["30", "30", "0", "0"],
    "8": ["10", "0", "0", "0"],
    "7": ["5", "0", "0", "0"],
    "6": ["0", "0", "0", "0"],
    "5": ["0", "0", "0", "0"],
    "4": ["0", "0", "0", "0"],
    "3": ["0", "0", "0", "0"],
    "2": ["0", "0", "0", "0"],
    "1": ["0", "0", "0", "0"],
}


async def clanstatsfn(ctx, tag, cocc):
    if tag == "":
        tag = await getsavedtag(ctx)
        if tag == False:
            return
    try:
        clan = await cocc.get_clan(tag)
    except:
        await errorimg(
            "The tag seems to be invalid Chief! Can you copy it again from the game and retry?",
            3,
            ctx,
            True,
        )
        return
    data = [
        {
            "count": 0,
            "war_stars": 0,
            "attack_wins": 0,
            "trophies": 0,
            "donations": 0,
            "Archer Queen": 0,
            "Barbarian King": 0,
            "Royal Champion": 0,
            "Grand Warden": 0,
            "Electro Owl": 0,
            "L.A.S.S.I": 0,
            "Mighty Yak": 0,
            "Unicorn": 0,
            "Frosty": 0,
            "Diggy": 0,
            "Poison Lizard": 0,
            "Pheonix": 0,
        },
        {
            "count": 0,
            "war_stars": 0,
            "attack_wins": 0,
            "trophies": 0,
            "donations": 0,
            "Archer Queen": 0,
            "Barbarian King": 0,
            "Royal Champion": 0,
            "Grand Warden": 0,
            "Electro Owl": 0,
            "L.A.S.S.I": 0,
            "Mighty Yak": 0,
            "Unicorn": 0,
            "Frosty": 0,
            "Diggy": 0,
            "Poison Lizard": 0,
            "Pheonix": 0,

        },
        {
            "count": 0,
            "war_stars": 0,
            "attack_wins": 0,
            "trophies": 0,
            "donations": 0,
            "Archer Queen": 0,
            "Barbarian King": 0,
            "Royal Champion": 0,
            "Grand Warden": 0,
            "Electro Owl": 0,
            "L.A.S.S.I": 0,
            "Mighty Yak": 0,
            "Unicorn": 0,
            "Frosty": 0,
            "Diggy": 0,
            "Poison Lizard": 0,
            "Pheonix": 0,
        },
        {
            "count": 0,
            "war_stars": 0,
            "attack_wins": 0,
            "trophies": 0,
            "donations": 0,
            "Archer Queen": 0,
            "Barbarian King": 0,
            "Royal Champion": 0,
            "Grand Warden": 0,
            "Electro Owl": 0,
            "L.A.S.S.I": 0,
            "Mighty Yak": 0,
            "Unicorn": 0,
            "Frosty": 0,
            "Diggy": 0,
            "Poison Lizard": 0,
            "Pheonix": 0,
        },
        {
            "count": 0,
            "war_stars": 0,
            "attack_wins": 0,
            "trophies": 0,
            "donations": 0,
            "Archer Queen": 0,
            "Barbarian King": 0,
            "Royal Champion": 0,
            "Grand Warden": 0,
            "Electro Owl": 0,
            "L.A.S.S.I": 0,
            "Mighty Yak": 0,
            "Unicorn": 0,
            "Frosty": 0,
            "Diggy": 0,
            "Poison Lizard": 0,
            "Pheonix": 0,
        },
        {
            "count": 0,
            "war_stars": 0,
            "attack_wins": 0,
            "trophies": 0,
            "donations": 0,
            "Archer Queen": 0,
            "Barbarian King": 0,
            "Royal Champion": 0,
            "Grand Warden": 0,
            "Electro Owl": 0,
            "L.A.S.S.I": 0,
            "Mighty Yak": 0,
            "Unicorn": 0,
            "Frosty": 0,
            "Diggy": 0,
            "Poison Lizard": 0,
            "Pheonix": 0,
        },
        {
            "count": 0,
            "war_stars": 0,
            "attack_wins": 0,
            "trophies": 0,
            "donations": 0,
            "Archer Queen": 0,
            "Barbarian King": 0,
            "Royal Champion": 0,
            "Grand Warden": 0,
            "Electro Owl": 0,
            "L.A.S.S.I": 0,
            "Mighty Yak": 0,
            "Unicorn": 0,
            "Frosty": 0,
            "Diggy": 0,
            "Poison Lizard": 0,
            "Pheonix": 0,
        },
        {
            "count": 0,
            "war_stars": 0,
            "attack_wins": 0,
            "trophies": 0,
            "donations": 0,
            "Archer Queen": 0,
            "Barbarian King": 0,
            "Royal Champion": 0,
            "Grand Warden": 0,
            "Electro Owl": 0,
            "L.A.S.S.I": 0,
            "Mighty Yak": 0,
            "Unicorn": 0,
            "Frosty": 0,
            "Diggy": 0,
            "Poison Lizard": 0,
            "Pheonix": 0,
        },
        {
            "count": 0,
            "war_stars": 0,
            "attack_wins": 0,
            "trophies": 0,
            "donations": 0,
            "Archer Queen": 0,
            "Barbarian King": 0,
            "Royal Champion": 0,
            "Grand Warden": 0,
            "Electro Owl": 0,
            "L.A.S.S.I": 0,
            "Mighty Yak": 0,
            "Unicorn": 0,
            "Frosty": 0,
            "Diggy": 0,
            "Poison Lizard": 0,
            "Pheonix": 0,
        },
        {
            "count": 0,
            "war_stars": 0,
            "attack_wins": 0,
            "trophies": 0,
            "donations": 0,
            "Archer Queen": 0,
            "Barbarian King": 0,
            "Royal Champion": 0,
            "Grand Warden": 0,
            "Electro Owl": 0,
            "L.A.S.S.I": 0,
            "Mighty Yak": 0,
            "Unicorn": 0,
            "Frosty": 0,
            "Diggy": 0,
            "Poison Lizard": 0,
            "Pheonix": 0,
        },
        {
            "count": 0,
            "war_stars": 0,
            "attack_wins": 0,
            "trophies": 0,
            "donations": 0,
            "Archer Queen": 0,
            "Barbarian King": 0,
            "Royal Champion": 0,
            "Grand Warden": 0,
            "Electro Owl": 0,
            "L.A.S.S.I": 0,
            "Mighty Yak": 0,
            "Unicorn": 0,
            "Frosty": 0,
            "Diggy": 0,
            "Poison Lizard": 0,
            "Pheonix": 0,
        },
        {
            "count": 0,
            "war_stars": 0,
            "attack_wins": 0,
            "trophies": 0,
            "donations": 0,
            "Archer Queen": 0,
            "Barbarian King": 0,
            "Royal Champion": 0,
            "Grand Warden": 0,
            "Electro Owl": 0,
            "L.A.S.S.I": 0,
            "Mighty Yak": 0,
            "Unicorn": 0,
            "Frosty": 0,
            "Diggy": 0,
            "Poison Lizard": 0,
            "Pheonix": 0,
        },
        {
            "count": 0,
            "war_stars": 0,
            "attack_wins": 0,
            "trophies": 0,
            "donations": 0,
            "Archer Queen": 0,
            "Barbarian King": 0,
            "Royal Champion": 0,
            "Grand Warden": 0,
            "Electro Owl": 0,
            "L.A.S.S.I": 0,
            "Mighty Yak": 0,
            "Unicorn": 0,
            "Frosty": 0,
            "Diggy": 0,
            "Poison Lizard": 0,
            "Pheonix": 0,
        },
        {
            "count": 0,
            "war_stars": 0,
            "attack_wins": 0,
            "trophies": 0,
            "donations": 0,
            "Archer Queen": 0,
            "Barbarian King": 0,
            "Royal Champion": 0,
            "Grand Warden": 0,
            "Electro Owl": 0,
            "L.A.S.S.I": 0,
            "Mighty Yak": 0,
            "Unicorn": 0,
            "Frosty": 0,
            "Diggy": 0,
            "Poison Lizard": 0,
            "Pheonix": 0,
        },
    ]
    async for player in clan.get_detailed_members():
        th = 14 - player.town_hall
        data[th]["th"] = player.town_hall
        data[th]["count"] += 1
        data[th]["war_stars"] += player.war_stars
        data[th]["attack_wins"] += player.attack_wins
        data[th]["trophies"] += player.trophies
        data[th]["donations"] += player.donations
        heroes = player.heroes
        pets = player.pets
        for i in heroes:
            try:
                data[th][i.name] += i.level
            except:
                continue
        for i in pets:
            try:
                data[th][i.name] += i.level
            except:
                continue
    newdata = []
    for i in range(len(data)):
        count = data[i]["count"]
        if count == 0:
            continue
        for key, value in data[i].items():
            if key == "count":
                data[i][key] = "x" + str(value)
            elif key == "th":
                data[i][key] = str(value)
            else:
                data[i][key] = str(ceil(value / count))
        newdata.append(data[i])

    thfont = ImageFont.truetype("utility/assets/thick.ttf", 15)
    thfont2 = ImageFont.truetype("utility/assets/thick.ttf", 20)
    lvlfont = ImageFont.truetype("utility/assets/thin.ttf", 18)
    bkimg = Image.open("utility/assets/comp/bk.png")
    aqimg = Image.open("utility/assets/comp/aq.png")
    gwimg = Image.open("utility/assets/comp/gw.png")
    rcimg = Image.open("utility/assets/comp/rc.png")
    lassiimg = Image.open("utility/assets/comp/lassi.png")
    owlimg = Image.open("utility/assets/comp/owl.png")
    yakimg = Image.open("utility/assets/comp/yak.png")
    unicornimg = Image.open("utility/assets/comp/unicorn.png")
    frostyimg = Image.open("utility/assets/comp/frosty.png")
    diggyimg = Image.open("utility/assets/comp/diggy.png")
    lizardimg = Image.open("utility/assets/comp/lizard.png")
    phoeniximg = Image.open("utility/assets/comp/phoenix.png")
    labelimg = Image.open("utility/assets/comp/label.png")

    bkimg1 = Image.open("utility/assets/comp/bkmax1.png")
    aqimg1 = Image.open("utility/assets/comp/aqmax1.png")
    gwimg1 = Image.open("utility/assets/comp/gwmax1.png")
    rcimg1 = Image.open("utility/assets/comp/rcmax1.png")
    bkimg2 = Image.open("utility/assets/comp/bkmax2.png")
    aqimg2 = Image.open("utility/assets/comp/aqmax2.png")
    gwimg2 = Image.open("utility/assets/comp/gwmax2.png")
    rcimg2 = Image.open("utility/assets/comp/rcmax2.png")
    lassiimg1 = Image.open("utility/assets/comp/lassimax.png")
    owlimg1 = Image.open("utility/assets/comp/owlmax.png")
    yakimg1 = Image.open("utility/assets/comp/yakmax.png")
    unicornimg1 = Image.open("utility/assets/comp/unicornmax.png")
    frostyimg1 = Image.open("utility/assets/comp/frostymax.png")
    diggyimg1 = Image.open("utility/assets/comp/diggymax.png")
    lizardimg1 = Image.open("utility/assets/comp/lizardmax.png")
    phoeniximg1 = Image.open("utility/assets/comp/phoenixmax.png")
    labelimg1 = Image.open("utility/assets/comp/label.png")

    files = []

    for i in range(len(newdata)):
        img = Image.open("utility/assets/comp/panel.png")
        draw = ImageDraw.Draw(img)
        thimg = Image.open(f"utility/assets/comp/{newdata[i]['th']}.png")
        img.paste(thimg, (14, 14), thimg)

        if newdata[i]["Barbarian King"] != "0":
            if newdata[i]["Barbarian King"] == "90":
                img.paste(bkimg1, (159, 17), bkimg1)
            elif maxherolvl[newdata[i]["th"]][0] == newdata[i]["Barbarian King"]:
                img.paste(bkimg2, (159, 17), bkimg2)
            else:
                img.paste(bkimg, (159, 17), bkimg)
            draw.text(
                (177, 84),
                newdata[i]["Barbarian King"],
                fill=(255, 255, 255),
                font=lvlfont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )
        if newdata[i]["Archer Queen"] != "0":
            if newdata[i]["Archer Queen"] == "90":
                img.paste(aqimg1, (225, 17), aqimg1)
            elif maxherolvl[newdata[i]["th"]][1] == newdata[i]["Archer Queen"]:
                img.paste(aqimg2, (225, 17), aqimg2)
            else:
                img.paste(aqimg, (225, 17), aqimg)
            draw.text(
                (243, 84),
                newdata[i]["Archer Queen"],
                fill=(255, 255, 255),
                font=lvlfont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )
        if newdata[i]["Grand Warden"] != "0":
            if newdata[i]["Grand Warden"] == "65":
                img.paste(gwimg1, (291, 17), gwimg1)
            elif maxherolvl[newdata[i]["th"]][2] == newdata[i]["Grand Warden"]:
                img.paste(gwimg2, (291, 17), gwimg2)
            else:
                img.paste(gwimg, (291, 17), gwimg)
            draw.text(
                (309, 84),
                newdata[i]["Grand Warden"],
                fill=(255, 255, 255),
                font=lvlfont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )
        if newdata[i]["Royal Champion"] != "0":
            if newdata[i]["Royal Champion"] == "40":
                img.paste(rcimg1, (357, 17), rcimg1)
            elif maxherolvl[newdata[i]["th"]][3] == newdata[i]["Royal Champion"]:
                img.paste(rcimg2, (357, 17), rcimg2)
            else:
                img.paste(rcimg, (357, 17), rcimg)
            draw.text(
                (375, 84),
                newdata[i]["Royal Champion"],
                fill=(255, 255, 255),
                font=lvlfont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )
        if newdata[i]["L.A.S.S.I"] != "0":
            if newdata[i]["L.A.S.S.I"] == "15":
                img.paste(lassiimg1, (159, 118), lassiimg1)
            else:
                img.paste(lassiimg, (159, 118), lassiimg)
            draw.text(
                (177, 167),
                newdata[i]["L.A.S.S.I"],
                fill=(255, 255, 255),
                font=lvlfont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )
        if newdata[i]["Electro Owl"] != "0":
            if newdata[i]["Electro Owl"] == "15":
                img.paste(owlimg1, (225, 118), owlimg1)
            else:
                img.paste(owlimg, (225, 118), owlimg)
            draw.text(
                (243, 167),
                newdata[i]["Electro Owl"],
                fill=(255, 255, 255),
                font=lvlfont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )
        if newdata[i]["Mighty Yak"] != "0":
            if newdata[i]["Mighty Yak"] == "15":
                img.paste(yakimg1, (291, 118), yakimg1)
            else:
                img.paste(yakimg, (291, 118), yakimg)
            draw.text(
                (309, 167),
                newdata[i]["Mighty Yak"],
                fill=(255, 255, 255),
                font=lvlfont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )
        if newdata[i]["Unicorn"] != "0":
            if newdata[i]["Unicorn"] == "15":
                img.paste(unicornimg1, (357, 118), unicornimg1)
            else:
                img.paste(unicornimg, (357, 118), unicornimg)
            draw.text(
                (375, 167),
                newdata[i]["Unicorn"],
                fill=(255, 255, 255),
                font=lvlfont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )
        if newdata[i]["Frosty"] != "0":
            if newdata[i]["Frosty"] == "10":
                img.paste(frostyimg1, (357, 118), frostyimg1)
            else:
                img.paste(frostyimg, (357, 118), frostyimg)
            draw.text(
                (375, 167),
                newdata[i]["Frosty"],
                fill=(255, 255, 255),
                font=lvlfont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )
        if newdata[i]["Diggy"] != "0":
            if newdata[i]["Diggy"] == "10":
                img.paste(diggyimg1, (357, 118), diggyimg1)
            else:
                img.paste(diggyimg, (357, 118), diggyimg)
            draw.text(
                (375, 167),
                newdata[i]["Diggy"],
                fill=(255, 255, 255),
                font=lvlfont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )
        if newdata[i]["Poison Lizard"] != "0":
            if newdata[i]["Poison Lizard"] == "10":
                img.paste(lizardimg1, (357, 118), lizardimg1)
            else:
                img.paste(lizardimg, (357, 118), lizardimg)
            draw.text(
                (375, 167),
                newdata[i]["Poison Lizard"],
                fill=(255, 255, 255),
                font=lvlfont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )
        if newdata[i]["Phoenix"] != "0":
            if newdata[i]["Phoenix"] == "10":
                img.paste(phoeniximg1, (357, 118), phoeniximg1)
            else:
                img.paste(phoeniximg, (357, 118), phoeniximg)
            draw.text(
                (375, 167),
                newdata[i]["Unicorn"],
                fill=(255, 255, 255),
                font=lvlfont,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )

        draw.text(
            (80, 35),
            newdata[i]["count"],
            fill=(0, 0, 0),
            font=thfont2,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (80, 33),
            newdata[i]["count"],
            fill=(255, 255, 255),
            font=thfont2,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (483, 34),
            newdata[i]["trophies"],
            fill=(255, 255, 255),
            font=thfont,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="lm",
        )
        draw.text(
            (483, 78),
            newdata[i]["war_stars"],
            fill=(255, 255, 255),
            font=thfont,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="lm",
        )
        draw.text(
            (483, 121),
            newdata[i]["attack_wins"],
            fill=(255, 255, 255),
            font=thfont,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="lm",
        )
        draw.text(
            (483, 164),
            newdata[i]["donations"],
            fill=(255, 255, 255),
            font=thfont,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="lm",
        )
        if i == 0:
            imglabel = Image.new("RGBA", (600, 253), color=(225, 225, 225, 0))
            imglabel.paste(img, (0, 55), img)
            imglabel.paste(labelimg, (0, 0), labelimg)
            draw = ImageDraw.Draw(imglabel)
            draw.text(
                (300, 32),
                clan.name,
                fill=(0, 0, 0),
                font=thfont2,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )
            draw.text(
                (300, 29),
                clan.name,
                fill=(255, 255, 255),
                font=thfont2,
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="mm",
            )
            img = imglabel
        with BytesIO() as image:
            img = img.convert("P", palette=Image.ADAPTIVE)
            img.save(image, "PNG")
            image.seek(0)
            files.append(discord_File(fp=image, filename=f"clan{i+1}.png"))
    await ctx.send(files=files)


supertroops = {
    1: ["Super Barbarian", "Barbarian", "11"],
    2: ["Super Archer", "Archer", "11"],
    3: ["Super Giant", "Giant", "11"],
    4: ["Sneaky Goblin", "Goblin", "9"],
    5: ["Super Wall Breaker", "Wall Breaker", "11"],
    6: ["Rocket Balloon", "Balloon", "10"],
    7: ["Super Wizard", "Wizard", "11"],
    8: ["Inferno Dragon", "Baby Dragon", "9"],
    9: ["Super Minion", "Minion", "11"],
    10: ["Super Valkyrie", "Valkyrie", "10"],
    11: ["Super Witch", "Witch", "6"],
    12: ["Ice Hound", "Lava Hound", "6"],
    13: ["Super Bowler", "Bowler", "7"],
    14: ["Super Dragon", "Dragon", "10"],
    15: ["Super Miner", "Miner", "9"],
    16: ["Super Hog Rider", "Hog Rider", "12"],
}


async def clansuperfn(troop, tag, ctx, cocc):
    if tag == "":
        tag = await getsavedtag(ctx)
        if tag == False:
            return
    try:
        clan = await cocc.get_clan(tag)
    except:
        await errorimg(
            "The tag seems to be invalid Chief! Can you copy it again from the game and retry?",
            3,
            ctx,
            True,
        )
        return
    data, id = [], troop
    async for player in clan.get_detailed_members():
        pdata = ["", 0]
        for troop in player.home_troops:
            if troop.name == supertroops[id][0] and troop.is_active == True:
                pdata[0] = player.name.encode("ascii", "ignore").decode()
            if troop.name == supertroops[id][1]:
                pdata[1] = troop.level
        if pdata[0] != "":
            data.append(pdata)
    if len(data) == 0:
        await errorimg(
            f"No one has boosted {supertroops[id][0]} right now in {clan.name} Chief!",
            1,
            ctx,
            True,
        )
        return
    data.sort(key=lambda x: x[1], reverse=True)

    troop, maxtlvl = id, supertroops[id][2]
    cname = clan.name
    files = []
    fontnum = ImageFont.truetype("utility/assets/thick.ttf", 15)
    fontname = ImageFont.truetype("utility/assets/thin.ttf", 16)
    fontclan = ImageFont.truetype("utility/assets/thick.ttf", 21)
    img = Image.open("utility/assets/super/panel.png")
    timg = Image.open(f"utility/assets/super/{troop}.png")
    timgmask = Image.open("utility/assets/super/troopmask.png")
    nimg = Image.open("utility/assets/super/namebg.png")
    nimgmask = Image.open("utility/assets/super/namemask.png")

    img.paste(timg, (15, 66), timgmask)
    draw = ImageDraw.Draw(img)
    draw.text(
        (300, 34),
        cname,
        fill=(0, 0, 0),
        font=fontclan,
        stroke_width=2,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )
    draw.text(
        (300, 31),
        cname,
        fill=(255, 255, 255),
        font=fontclan,
        stroke_width=2,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )

    if len(data) <= 7:
        firstnum = len(data)
    else:
        firstnum = 7
    for i in range(firstnum):
        name = data[i][0]
        level = str(data[i][1])
        if level == maxtlvl:
            lvlcolour = (248, 223, 122)
        else:
            lvlcolour = (255, 255, 255)
        img.paste(nimg, (305, 81 + i * 36), nimgmask)
        draw.text(
            (350, 104 + i * 36),
            level,
            fill=(0, 0, 0),
            font=fontnum,
            stroke_width=1,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (350, 102 + i * 36),
            level,
            fill=lvlcolour,
            font=fontnum,
            stroke_width=1,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (382, 101 + i * 36), name, fill=(55, 55, 55), font=fontname, anchor="lm"
        )

    with BytesIO() as image:
        img = img.convert("P", palette=Image.ADAPTIVE)
        img.save(image, "PNG")
        image.seek(0)
        files.append(discord_File(fp=image, filename=f"super1.png"))

    if len(data) > 7:
        data = data[7:]
        for j in range(ceil(len(data) / 14)):
            newdata = data[j * 14 : 14 + j * 14]
            img = Image.open("utility/assets/super/panelnext.png")
            draw = ImageDraw.Draw(img)

            lefty, righty = 0, 0
            for i in range(len(newdata)):
                if i % 2 == 0:
                    x1, x2, x3 = 20, 65, 97
                    lefty += 36
                    y = lefty
                else:
                    x1, x2, x3 = 305, 350, 382
                    righty += 36
                    y = righty

                name = newdata[i][0]
                level = str(newdata[i][1])
                if level == maxtlvl:
                    lvlcolour = (248, 223, 122)
                else:
                    lvlcolour = (255, 255, 255)
                img.paste(nimg, (x1, -18 + y), nimgmask)
                draw.text(
                    (x2, 5 + y),
                    level,
                    fill=(0, 0, 0),
                    font=fontnum,
                    stroke_width=1,
                    stroke_fill=(0, 0, 0),
                    anchor="mm",
                )
                draw.text(
                    (x2, 3 + y),
                    level,
                    fill=lvlcolour,
                    font=fontnum,
                    stroke_width=1,
                    stroke_fill=(0, 0, 0),
                    anchor="mm",
                )
                draw.text(
                    (x3, 2 + y), name, fill=(55, 55, 55), font=fontname, anchor="lm"
                )
            with BytesIO() as image:
                img = img.convert("P", palette=Image.ADAPTIVE)
                img.save(image, "PNG")
                image.seek(0)
                files.append(discord_File(fp=image, filename=f"super{j+2}.png"))
    await ctx.send(files=files)
