import discord
from discord.ext import commands
import os
import asyncio
from datetime import datetime
import traceback
from config import TOKEN, PREFIX, WELCOME_CHANNEL_ID, LOG_CHANNEL_ID
from utils.image_generator import generate_welcome_card
from utils.error_handler import setup_error_handler
import logging

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('WelcomeBot')

# Bot intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

# Bot initialization
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# Error handler setup
setup_error_handler(bot, logger)

@bot.event
async def on_ready():
    """Bot ready event"""
    try:
        logger.info(f'✅ Bot logged in as {bot.user.name} (ID: {bot.user.id})')
        logger.info(f'📊 Connected to {len(bot.guilds)} servers')
        logger.info(f'👥 Watching {len(bot.users)} users')
        
        # Set bot status
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(bot.guilds)} servers | {PREFIX}help"
            )
        )
        logger.info('✨ Bot is ready!')
    except Exception as e:
        logger.error(f'Error in on_ready: {e}')
        logger.error(traceback.format_exc())

@bot.event
async def on_member_join(member):
    """Welcome new members with custom card"""
    try:
        guild = member.guild
        logger.info(f'👋 New member joined: {member.name} in {guild.name}')
        
        # Get welcome channel
        welcome_channel = None
        if WELCOME_CHANNEL_ID:
            welcome_channel = bot.get_channel(int(WELCOME_CHANNEL_ID))
        
        if not welcome_channel:
            # Find channel with 'welcome' in name
            for channel in guild.text_channels:
                if 'welcome' in channel.name.lower():
                    welcome_channel = channel
                    break
        
        if not welcome_channel:
            # Use system channel
            welcome_channel = guild.system_channel
        
        if not welcome_channel:
            logger.warning(f'No welcome channel found for {guild.name}')
            return
        
        # Generate welcome card
        logger.info(f'🎨 Generating welcome card for {member.name}...')
        image_path = await generate_welcome_card(member, guild)
        
        if not image_path or not os.path.exists(image_path):
            logger.error(f'Failed to generate welcome card for {member.name}')
            # Send text welcome as fallback
            await welcome_channel.send(f'Welcome to **{guild.name}**, {member.mention}! 🎉')
            return
        
        # Send welcome message with image
        file = discord.File(image_path, filename='welcome.png')
        
        embed = discord.Embed(
            description=f'Welcome to **{guild.name}**, {member.mention}! 🎉\n\n'
                       f'You are member **#{guild.member_count}**',
            color=discord.Color.blue()
        )
        embed.set_image(url='attachment://welcome.png')
        embed.set_footer(text=f'Joined at {datetime.utcnow().strftime("%d %b %Y, %I:%M %p UTC")}')
        
        await welcome_channel.send(embed=embed, file=file)
        logger.info(f'✅ Welcome card sent for {member.name}')
        
        # Cleanup image file
        try:
            await asyncio.sleep(2)
            os.remove(image_path)
        except Exception as e:
            logger.warning(f'Failed to cleanup image: {e}')
            
    except discord.Forbidden:
        logger.error(f'Missing permissions in {guild.name}')
    except Exception as e:
        logger.error(f'Error in on_member_join: {e}')
        logger.error(traceback.format_exc())

@bot.command(name='testwelcome', aliases=['tw', 'welcometest'])
@commands.has_permissions(manage_guild=True)
async def test_welcome(ctx, member: discord.Member = None):
    """Test welcome message for a member"""
    try:
        if not member:
            member = ctx.author
        
        logger.info(f'Testing welcome for {member.name} by {ctx.author.name}')
        
        # Generate welcome card
        processing_msg = await ctx.send(f'🎨 Generating welcome card for {member.mention}...')
        
        image_path = await generate_welcome_card(member, ctx.guild)
        
        if not image_path or not os.path.exists(image_path):
            await processing_msg.edit(content='❌ Failed to generate welcome card!')
            return
        
        # Send welcome card
        file = discord.File(image_path, filename='welcome.png')
        
        embed = discord.Embed(
            description=f'**Test Welcome Card**\n\n'
                       f'Member: {member.mention}\n'
                       f'Member Count: **#{ctx.guild.member_count}**',
            color=discord.Color.green()
        )
        embed.set_image(url='attachment://welcome.png')
        embed.set_footer(text=f'Tested by {ctx.author.name}')
        
        await processing_msg.delete()
        await ctx.send(embed=embed, file=file)
        logger.info(f'✅ Test welcome sent for {member.name}')
        
        # Cleanup
        try:
            await asyncio.sleep(2)
            os.remove(image_path)
        except:
            pass
            
    except commands.MissingPermissions:
        await ctx.send('❌ You need **Manage Server** permission to use this command!')
    except Exception as e:
        logger.error(f'Error in test_welcome: {e}')
        await ctx.send(f'❌ Error: {str(e)}')

@bot.command(name='setwelcome', aliases=['sw'])
@commands.has_permissions(manage_guild=True)
async def set_welcome_channel(ctx, channel: discord.TextChannel = None):
    """Set welcome channel (Admin only)"""
    try:
        if not channel:
            channel = ctx.channel
        
        # Here you can save to database
        # For now just inform
        embed = discord.Embed(
            title='✅ Welcome Channel Set',
            description=f'Welcome messages will be sent to {channel.mention}',
            color=discord.Color.green()
        )
        embed.add_field(name='Note', value='Make sure bot has permissions to send messages and attach files in that channel!')
        
        await ctx.send(embed=embed)
        logger.info(f'Welcome channel set to {channel.name} in {ctx.guild.name}')
        
    except commands.MissingPermissions:
        await ctx.send('❌ You need **Manage Server** permission!')
    except Exception as e:
        logger.error(f'Error in set_welcome_channel: {e}')
        await ctx.send(f'❌ Error: {str(e)}')

@bot.command(name='help', aliases=['h'])
async def help_command(ctx):
    """Show help menu"""
    try:
        embed = discord.Embed(
            title='🤖 Welcome Bot Commands',
            description='Advanced Discord Welcome Bot with Custom Cards',
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name='📋 General Commands',
            value=f'`{PREFIX}help` - Show this menu\n'
                  f'`{PREFIX}ping` - Check bot latency\n'
                  f'`{PREFIX}stats` - Show bot statistics',
            inline=False
        )
        
        embed.add_field(
            name='👋 Welcome Commands (Admin)',
            value=f'`{PREFIX}testwelcome [@member]` - Test welcome card\n'
                  f'`{PREFIX}setwelcome [#channel]` - Set welcome channel',
            inline=False
        )
        
        embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.display_avatar.url)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        logger.error(f'Error in help_command: {e}')
        await ctx.send('❌ Error showing help menu!')

@bot.command(name='ping')
async def ping(ctx):
    """Check bot latency"""
    try:
        latency = round(bot.latency * 1000)
        
        embed = discord.Embed(
            title='🏓 Pong!',
            description=f'Bot Latency: **{latency}ms**',
            color=discord.Color.green() if latency < 200 else discord.Color.orange()
        )
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        logger.error(f'Error in ping: {e}')
        await ctx.send('❌ Error checking ping!')

@bot.command(name='stats', aliases=['statistics', 'info'])
async def stats(ctx):
    """Show bot statistics"""
    try:
        embed = discord.Embed(
            title='📊 Bot Statistics',
            color=discord.Color.blue()
        )
        
        embed.add_field(name='Servers', value=str(len(bot.guilds)), inline=True)
        embed.add_field(name='Users', value=str(len(bot.users)), inline=True)
        embed.add_field(name='Latency', value=f'{round(bot.latency * 1000)}ms', inline=True)
        
        embed.set_thumbnail(url=bot.user.display_avatar.url)
        embed.set_footer(text=f'Requested by {ctx.author.name}')
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        logger.error(f'Error in stats: {e}')
        await ctx.send('❌ Error showing statistics!')

@bot.event
async def on_command_error(ctx, error):
    """Global command error handler"""
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('❌ You don\'t have permission to use this command!')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'❌ Missing required argument! Use `{PREFIX}help` for command usage.')
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f'❌ Invalid argument! Use `{PREFIX}help` for command usage.')
    else:
        logger.error(f'Command error: {error}')
        logger.error(traceback.format_exc())
        await ctx.send('❌ An error occurred while executing the command!')

# Run bot
if __name__ == '__main__':
    try:
        logger.info('🚀 Starting bot...')
        bot.run(TOKEN)
    except Exception as e:
        logger.critical(f'Failed to start bot: {e}')
        logger.critical(traceback.format_exc())
