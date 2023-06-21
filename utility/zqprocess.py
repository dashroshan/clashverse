from math import ceil as math_ceil
from io import BytesIO
from discord import File as discord_File
from utility.errorimage import errorimg
from PIL import Image, ImageDraw, ImageFont

aura = [
    [0, 0],
    [0.200, 70],
    [0.211, 76],
    [0.222, 82],
    [0.233, 88],
    [0.244, 94],
    [0.256, 101],
    [0.268, 108],
    [0.281, 116],
    [0.295, 125],
    [0.310, 135],
    [0.326, 146],
    [0.343, 158],
    [0.361, 171],
    [0.380, 185],
    [0.400, 200],
    [0.420, 215],
    [0.440, 230],
    [0.460, 245],
    [0.480, 260],
    [0.500, 275],
    [0.520, 290],
    [0.540, 305],
    [0.560, 320],
    [0.580, 335],
    [0.600, 350],
    [0.620, 365],
    [0.640, 380],
    [0.660, 395],
    [0.680, 410],
    [0.700, 425],
    [0.720, 440],
    [0.740, 455],
    [0.760, 470],
    [0.780, 485],
    [0.800, 500],
    [0.820, 515],
    [0.840, 530],
    [0.860, 545],
    [0.880, 560],
    [0.900, 575],
]

hp = [
    {"name": "0 Ignore", "hp": [1]},
    {
        "name": "Archer Queen",
        "hp": [
            85, 725, 740, 755, 771, 787, 804, 821, 838, 856, 874, 892, 911, 930,
            949, 969, 990, 1010, 1032, 1053, 1076, 1098, 1121, 1145, 1169, 1193,
            1218, 1244, 1270, 1297, 1324, 1352, 1380, 1409, 1439, 1469, 1500,
            1532, 1564, 1597, 1630, 1664, 1699, 1735, 1771, 1809, 1847, 1885,
            1925, 1965, 2007, 2058, 2110, 2163, 2218, 2274, 2331, 2390, 2450,
            2512, 2575, 2639, 2705, 2773, 2842, 2913, 2980, 3040, 3095, 3145,
            3190, 3230, 3270, 3310, 3350, 3390, 3425, 3460, 3495, 3530, 3565,
            3600, 3630, 3660, 3690, 3720,
        ],
    },
    {
        "name": "Barbarian King",
        "hp": [
            85, 1700, 1742, 1786, 1830, 1876, 1923, 1971, 2020, 2071, 2123,
            2176, 2230, 2286, 2343, 2402, 2462, 2523, 2586, 2651, 2717, 2785,
            2855, 2926, 2999, 3074, 3151, 3230, 3311, 3394, 3478, 3565, 3655,
            3746, 3840, 3936, 4034, 4135, 4238, 4344, 4453, 4564, 4678, 4795,
            4915, 5038, 5164, 5293, 5425, 5561, 5700, 5843, 5990, 6140, 6294,
            6452, 6614, 6780, 6950, 7124, 7303, 7486, 7673, 7865, 8062, 8264,
            8470, 8680, 8890, 9100, 9300, 9500, 9700, 9900, 10100, 10300, 10490,
            10680, 10870, 11060, 11250, 11400, 11550, 11700, 11850, 12000,
        ],
    },
    {
        "name": "Royal Champion",
        "hp": [
            35, 2950, 3000, 3050, 3100, 3150, 3200, 3250, 3300, 3350, 3400,
            3450, 3500, 3550, 3600, 3650, 3700, 3750, 3800, 3850, 3900, 3940,
            3980, 4020, 4060, 4100, 4140, 4180, 4220, 4260, 4300, 4330, 4360,
            4390, 4420, 4450,
        ],
    },
    {
        "name": "Grand Warden",
        "hp": [
            60, 1000, 1021, 1042, 1064, 1086, 1108, 1131, 1155, 1180, 1206,
            1233, 1261, 1290, 1320, 1350, 1380, 1410, 1440, 1470, 1500, 1530,
            1561, 1593, 1625, 1658, 1692, 1726, 1761, 1797, 1833, 1870, 1908,
            1947, 1986, 2026, 2067, 2109, 2152, 2196, 2240, 2260, 2280, 2300,
            2320, 2340, 2360, 2380, 2400, 2420, 2440, 2460, 2480, 2500, 2520,
            2540, 2560, 2580, 2600, 2620, 2640,
        ],
    },
    {
        "name": "Eagle Artillery",
        "hp": [5, 4000, 4400, 4800, 5200, 5600],
    },
    {
        "name": "Scattershot",
        "hp": [3, 3600, 4200, 4800],
    },
    {
        "name": "Inferno Tower",
        "hp": [9, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3700, 4000],
    },
    {
        "name": "X-Bow",
        "hp": [10, 1500, 1900, 2300, 2700, 3100, 3500, 3900, 4200, 4500, 4700],
    },
    {
        "name": "Air Defense",
        "hp": [
            13, 800, 850, 900, 950, 1000, 1050, 1100, 1210, 1300, 1400, 1500,
            1650, 1750,
        ],
    },
    {
        "name": "Air Sweeper",
        "hp": [7, 750, 800, 850, 900, 950, 1000, 1050],
    },
    {
        "name": "Wizard Tower",
        "hp": [
            15, 620, 650, 680, 730, 840, 960, 1200, 1440, 1680, 2000, 2240,
            2480, 2700, 2900, 3000,
        ],
    },
    {
        "name": "Hidden Tesla",
        "hp": [
            13, 600, 630, 660, 690, 730, 770, 810, 850, 900, 980, 1100, 1200,
            1350,
        ],
    },
    {
        "name": "Builder's Hut",
        "hp": [4, 250, 1000, 1300, 1600],
    },
    {
        "name": "Archer Tower",
        "hp": [
            21, 380, 420, 460, 500, 540, 580, 630, 690, 750, 810, 890, 970,
            1050, 1130, 1230, 1330, 1410, 1510, 1600, 1700, 1800,
        ],
    },
    {
        "name": "Cannon",
        "hp": [
            21, 420, 470, 520, 570, 620, 670, 730, 800, 880, 960, 1060, 1160,
            1260, 1380, 1500, 1620, 1740, 1870, 2000, 2150, 2250,
        ],
    },
    {
        "name": "Bomb Tower",
        "hp": [10, 650, 700, 750, 850, 1050, 1300, 1600, 1900, 2300, 2500],
    },
    {
        "name": "Mortar",
        "hp": [
            15, 400, 450, 500, 550, 600, 650, 700, 800, 950, 1100, 1300, 1500,
            1700, 1950, 2150,
        ],
    },
    {
        "name": "Spell Tower",
        "hp": [
            3, 2500, 2800, 3100,
        ],
    },
    {
        "name": "Monolith",
        "hp": [
            2, 4747, 5050,
        ],
    },
]

dmg = [
    [5, 14.5, 17, 21, 25, 29],
    [10, 150, 180, 210, 240, 270, 320, 400, 480, 560, 600],
]

font = ImageFont.truetype("utility/assets/thick.ttf", 18)
zapimg = Image.open("utility/assets/zapquake/zqzap.png")
quakeimg = Image.open("utility/assets/zapquake/zqquake.png")
maximg = Image.open("utility/assets/zapquake/zqmax.png")


async def img1(
        icount,
        zap,
        zaplvl,
        quake,
        quakelvl,
        cczap,
        cczaplvl,
        ccquake,
        ccquakelvl,
        bname,
        blvl,
):
    img = Image.open("utility/assets/zapquake/zqtabfirst.png")
    draw = ImageDraw.Draw(img)

    header = bname + " : LVL " + str(blvl)
    draw.text(
        (299, 32),
        header,
        fill=(0, 0, 0),
        font=font,
        stroke_width=2,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )
    draw.text(
        (299, 29),
        header,
        fill=(255, 255, 255),
        font=font,
        stroke_width=2,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )

    if zap != 0 or quake != 0:
        s1max = False
        if zap != 0:
            if zaplvl == 10:
                s1max = True
            s1img = zapimg
            s1num = "x" + str(zap)
            s1lvl = str(zaplvl)
        else:
            if quakelvl == 5:
                s1max = True
            s1img = quakeimg
            s1num = "x" + str(quake)
            s1lvl = str(quakelvl)
        img.paste(s1img, (55, 119), s1img)
        if s1max == True:
            img.paste(maximg, (62, 213), maximg)
        draw.text(
            (108, 138),
            s1num,
            fill=(0, 0, 0),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (108, 135),
            s1num,
            fill=(255, 255, 255),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (78, 237),
            s1lvl,
            fill=(255, 255, 255),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )

    if quake != 0 and zap != 0:
        s2max = False
        if quakelvl == 5:
            s2max = True
        s2num = "x" + str(quake)
        s2lvl = str(quakelvl)
        img.paste(quakeimg, (170, 119), quakeimg)
        if s2max == True:
            img.paste(maximg, (177, 213), maximg)
        draw.text(
            (223, 138),
            s2num,
            fill=(0, 0, 0),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (223, 135),
            s2num,
            fill=(255, 255, 255),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (192, 237),
            s2lvl,
            fill=(255, 255, 255),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )

    if cczap != 0 or ccquake != 0:
        s3max = False
        if cczap != 0:
            if cczaplvl == 10:
                s3max = True
            s3img = zapimg
            s3num = "x" + str(cczap)
            s3lvl = str(cczaplvl)
        else:
            if ccquakelvl == 5:
                s3max = True
            s3img = quakeimg
            s3num = "x" + str(ccquake)
            s3lvl = str(ccquakelvl)
        img.paste(s3img, (319, 119), s3img)
        if s3max == True:
            img.paste(maximg, (326, 213), maximg)
        draw.text(
            (372, 138),
            s3num,
            fill=(0, 0, 0),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (372, 135),
            s3num,
            fill=(255, 255, 255),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (342, 237),
            s3lvl,
            fill=(255, 255, 255),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )

    if ccquake != 0 and cczap != 0:
        s4max = False
        if ccquakelvl == 5:
            s4max = True
        s4num = "x" + str(ccquake)
        s4lvl = str(ccquakelvl)
        img.paste(quakeimg, (434, 119), quakeimg)
        if s4max == True:
            img.paste(maximg, (441, 213), maximg)
        draw.text(
            (487, 138),
            s4num,
            fill=(0, 0, 0),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (487, 135),
            s4num,
            fill=(255, 255, 255),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (457, 237),
            s4lvl,
            fill=(255, 255, 255),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )

    with BytesIO() as image:
        img = img.convert("P", palette=Image.ADAPTIVE)
        img.save(image, "PNG")
        image.seek(0)
        return discord_File(fp=image, filename=f"zqcombo{icount}.png")


async def img2(
        icount, zap, zaplvl, quake, quakelvl, cczap, cczaplvl, ccquake, ccquakelvl
):
    img = Image.open("utility/assets/zapquake/zqtabrest.png")
    draw = ImageDraw.Draw(img)

    if zap != 0 or quake != 0:
        s1max = False
        if zap != 0:
            if zaplvl == 10:
                s1max = True
            s1img = zapimg
            s1num = "x" + str(zap)
            s1lvl = str(zaplvl)
        else:
            if quakelvl == 5:
                s1max = True
            s1img = quakeimg
            s1num = "x" + str(quake)
            s1lvl = str(quakelvl)
        img.paste(s1img, (55, 16), s1img)
        if s1max == True:
            img.paste(maximg, (62, 110), maximg)
        draw.text(
            (108, 35),
            s1num,
            fill=(0, 0, 0),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (108, 32),
            s1num,
            fill=(255, 255, 255),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (78, 134),
            s1lvl,
            fill=(255, 255, 255),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )

    if quake != 0 and zap != 0:
        s2max = False
        if quakelvl == 5:
            s2max = True
        s2num = "x" + str(quake)
        s2lvl = str(quakelvl)
        img.paste(quakeimg, (170, 16), quakeimg)
        if s2max == True:
            img.paste(maximg, (177, 110), maximg)
        draw.text(
            (223, 35),
            s2num,
            fill=(0, 0, 0),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (223, 32),
            s2num,
            fill=(255, 255, 255),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (192, 134),
            s2lvl,
            fill=(255, 255, 255),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )

    if cczap != 0 or ccquake != 0:
        s3max = False
        if cczap != 0:
            if cczaplvl == 10:
                s3max = True
            s3img = zapimg
            s3num = "x" + str(cczap)
            s3lvl = str(cczaplvl)
        else:
            if ccquakelvl == 5:
                s3max = True
            s3img = quakeimg
            s3num = "x" + str(ccquake)
            s3lvl = str(ccquakelvl)
        img.paste(s3img, (319, 16), s3img)
        if s3max == True:
            img.paste(maximg, (326, 110), maximg)
        draw.text(
            (372, 35),
            s3num,
            fill=(0, 0, 0),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (372, 32),
            s3num,
            fill=(255, 255, 255),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (342, 134),
            s3lvl,
            fill=(255, 255, 255),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )

    if ccquake != 0 and cczap != 0:
        s4max = False
        if ccquakelvl == 5:
            s4max = True
        s4num = "x" + str(ccquake)
        s4lvl = str(ccquakelvl)
        img.paste(quakeimg, (434, 16), quakeimg)
        if s4max == True:
            img.paste(maximg, (441, 110), maximg)
        draw.text(
            (487, 35),
            s4num,
            fill=(0, 0, 0),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (487, 32),
            s4num,
            fill=(255, 255, 255),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )
        draw.text(
            (457, 134),
            s4lvl,
            fill=(255, 255, 255),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="mm",
        )

    with BytesIO() as image:
        img = img.convert("P", palette=Image.ADAPTIVE)
        img.save(image, "PNG")
        image.seek(0)
        return discord_File(fp=image, filename=f"zqcombo{icount}.png")


async def zqprocess(ctx, bid, lvl, zap, eq, ccspc, cczap, cceq, warden=0):
    name = hp[bid]["name"]
    total_lvl = hp[bid]["hp"][0]
    # checks for valid parameters
    if lvl > total_lvl:  # defense level given exceeds in-game levels
        await errorimg(f"The {name} has only {total_lvl} levels Chief!", 3, ctx, True)
        return
    if lvl < 1:  # 0 or -ve level
        await errorimg(
            f"The {name} level doesn't appear to be valid Chief!", 3, ctx, True
        )
        return
    if (
            warden > 60 or warden < 0
    ):  # enemy warden level given exceeds in-game levels or negetive
        await errorimg(
            "The enemy warden level doesn't appear to be valid Chief!", 3, ctx, True
        )
        return

    data = getCombos(bid, lvl, zap, eq, ccspc, cczap, cceq, warden)

    if len(data) == 0:
        await errorimg(
            f"Oh, no! The {name} cannot be taken down with any of your zapquake combos Chief!",
            4,
            ctx,
            True,
        )
        return

    count = 0
    files = []
    for j in data:
        count += 1
        if count == 1:
            file = await img1(
                count, j[0], zap, j[1], eq, j[2], cczap, j[3], cceq, name, lvl
            )
            files.append(file)
        else:
            file = await img2(count, j[0], zap, j[1], eq, j[2], cczap, j[3], cceq)
            files.append(file)
    await ctx.send(files=files)


def adjustWardenAura(buildingHp, wardenLvl, buildingId):
    if buildingId > 3:
        return buildingHp
    if wardenLvl > 40:
        wardenLvl = 40
    hpBoost = buildingHp * aura[wardenLvl][0]
    hpBoostMax = aura[wardenLvl][1]
    if hpBoost > hpBoostMax:
        hpBoost = hpBoostMax
    return hpBoost + buildingHp


def getCombos(
        buildingId, buildingLvl, zapLvl, eqLvl, ccSpace, ccZapLvl, ccEqLvl, wardenLvl
):
    buildingHp = adjustWardenAura(hp[buildingId]["hp"][buildingLvl], wardenLvl, buildingId)
    zapDmg = dmg[1][zapLvl]
    ccZapDmg = dmg[1][ccZapLvl]
    eqDmg = dmg[0][eqLvl]
    ccEqDmg = dmg[0][ccEqLvl]
    combos = []
    isHero = buildingId < 4

    for z in range(15):
        for e in range(15):
            for cz in range(ccSpace + 1):
                for ce in range(ccSpace + 1):
                    if z + e + cz + ce <= 14 and ((isHero and e == 0 and ce == 0) or not isHero) and (
                            cz + ce <= ccSpace):
                        combos.append([z + e + cz + ce, z, e, cz, ce, cz + ce])

    validCombos = []
    for combo in combos:
        dmgByEq = 0
        for ccEq in range(1, combo[4] + 1):
            dmgByEq += buildingHp * (ccEqDmg / (2 * ccEq - 1)) / 100
        for eq in range(1, combo[2] + 1):
            dmgByEq += buildingHp * (eqDmg / (2 * (combo[4] + eq) - 1)) / 100
        dmgByZap = combo[1] * zapDmg + combo[3] * ccZapDmg
        if dmgByEq + dmgByZap >= buildingHp:
            validCombos.append(combo)

    validCombos = sorted(validCombos, key=lambda x: [x[0], x[5]], reverse=False)
    minimumCombos = [
        [combo[1], combo[2], combo[3], combo[4]]
        for combo in validCombos
        if combo[0] == validCombos[0][0] and combo[5] == validCombos[0][5]
    ]
    return minimumCombos
