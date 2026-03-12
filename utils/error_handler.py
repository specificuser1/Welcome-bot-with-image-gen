import discord
from discord.ext import commands
import traceback
import sys

def setup_error_handler(bot, logger):
    """Setup global error handler for bot"""
    
    @bot.event
    async def on_error(event, *args, **kwargs):
        """Handle general bot errors"""
        logger.error(f'Error in event {event}:')
        logger.error(traceback.format_exc())
        
        # Try to log to log channel if configured
        try:
            from config import LOG_CHANNEL_ID
            if LOG_CHANNEL_ID:
                channel = bot.get_channel(int(LOG_CHANNEL_ID))
                if channel:
                    embed = discord.Embed(
                        title='⚠️ Bot Error',
                        description=f'Error in event: `{event}`',
                        color=discord.Color.red()
                    )
                    embed.add_field(
                        name='Error',
                        value=f'```py\n{str(sys.exc_info()[1])[:1000]}\n```',
                        inline=False
                    )
                    await channel.send(embed=embed)
        except:
            pass
    
    @bot.event
    async def on_command_error(ctx, error):
        """Handle command errors"""
        # Ignore command not found
        if isinstance(error, commands.CommandNotFound):
            return
        
        # Missing permissions
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('❌ You don\'t have permission to use this command!')
            return
        
        # Missing required argument
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'❌ Missing required argument: `{error.param.name}`')
            return
        
        # Bad argument
        if isinstance(error, commands.BadArgument):
            await ctx.send('❌ Invalid argument provided!')
            return
        
        # Command on cooldown
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'⏱️ This command is on cooldown. Try again in {error.retry_after:.1f}s')
            return
        
        # Bot missing permissions
        if isinstance(error, commands.BotMissingPermissions):
            missing = ', '.join(error.missing_permissions)
            await ctx.send(f'❌ I need the following permissions: `{missing}`')
            return
        
        # Log unexpected errors
        logger.error(f'Command error in {ctx.command}:')
        logger.error(''.join(traceback.format_exception(type(error), error, error.__traceback__)))
        
        await ctx.send('❌ An unexpected error occurred! The error has been logged.')
    
    logger.info('✅ Error handler setup complete')
