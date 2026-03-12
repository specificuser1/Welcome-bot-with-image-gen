import discord
from discord.ext import commands
from config import WELCOME_CHANNEL_ID
from image_creator import create_welcome_image

class Welcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):

        try:
            channel = member.guild.get_channel(WELCOME_CHANNEL_ID)

            img = await create_welcome_image(member)

            file = discord.File(img, filename="welcome.png")

            await channel.send(
                f"Welcome {member.mention} to **{member.guild.name}**",
                file=file
            )

        except Exception as e:
            print("WELCOME ERROR:", e)

    @commands.hybrid_command(name="testwelcome")
    async def testwelcome(self, ctx):

        try:
            member = ctx.author

            img = await create_welcome_image(member)

            file = discord.File(img, filename="welcome.png")

            channel = self.bot.get_channel(WELCOME_CHANNEL_ID)

            await channel.send(
                f"Test Welcome for {member.mention}",
                file=file
            )

        except Exception as e:
            await ctx.send(f"Error: {e}")
