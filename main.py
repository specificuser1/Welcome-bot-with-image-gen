import discord
from discord.ext import commands
from config import TOKEN
import welcome

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Bot Ready | {bot.user}")

bot.add_cog(welcome.Welcome(bot))

bot.run(TOKEN)
