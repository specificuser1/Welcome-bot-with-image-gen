import discord
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io
from datetime import datetime

async def create_welcome_image(member):

    width = 1000
    height = 400

    background = Image.new("RGBA", (width, height), (30,30,30))

    draw = ImageDraw.Draw(background)

    font_big = ImageFont.load_default()
    font_small = ImageFont.load_default()

    # download avatar
    async with aiohttp.ClientSession() as session:
        async with session.get(member.display_avatar.url) as resp:
            avatar_bytes = await resp.read()

    avatar = Image.open(io.BytesIO(avatar_bytes)).resize((200,200))

    background.paste(avatar,(40,100))

    member_number = member.guild.member_count

    text = [
        f"Name: {member}",
        f"User ID: {member.id}",
        f"Member #: {member_number}",
        f"Joined: {member.joined_at.date()}",
        f"Account Created: {member.created_at.date()}"
    ]

    y = 120
    for t in text:
        draw.text((300,y), t, font=font_big, fill=(255,255,255))
        y += 40

    buffer = io.BytesIO()
    background.save(buffer, "PNG")
    buffer.seek(0)

    return buffer
