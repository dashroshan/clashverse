from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from discord import File as discord_File


async def errorimg(text, id, ctx, linebreak):
    if linebreak == True:
        textnew, line, text = "", "", text.split()
        for i in text:
            if len(line) + len(i) <= 23:
                line += " " + i
            else:
                textnew += line + "\n"
                line = i
        if len(line) != 0:
            textnew += line
    else:
        textnew = text
    font = ImageFont.truetype("utility/assets/thick.ttf", 17)
    img = Image.open(f"utility/assets/msg{id}.png")
    draw = ImageDraw.Draw(img)
    draw.text(
        (398, 175),
        textnew,
        fill=(55, 55, 55),
        font=font,
        anchor="mm",
        align="center",
        spacing=5,
    )
    with BytesIO() as image:
        img = img.convert("P", palette=Image.ADAPTIVE)
        img.save(image, "PNG")
        image.seek(0)
        await ctx.send(file=discord_File(fp=image, filename=f"clashverse0{id}.png"))
