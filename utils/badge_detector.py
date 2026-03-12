import discord
import logging

logger = logging.getLogger('BadgeDetector')

def get_user_badges(member: discord.Member):
    """Detect and return user's Discord badges"""
    badges = []
    
    try:
        public_flags = member.public_flags
        
        # Check all available badges
        if public_flags.staff:
            badges.append('staff')
            
        if public_flags.partner:
            badges.append('partner')
            
        if public_flags.hypesquad:
            badges.append('hypesquad')
            
        if public_flags.hypesquad_bravery:
            badges.append('hypesquad_bravery')
            
        if public_flags.hypesquad_brilliance:
            badges.append('hypesquad_brilliance')
            
        if public_flags.hypesquad_balance:
            badges.append('hypesquad_balance')
            
        if public_flags.bug_hunter:
            badges.append('bug_hunter')
            
        if public_flags.bug_hunter_level_2:
            badges.append('bug_hunter_level_2')
            
        if public_flags.verified_bot_developer:
            badges.append('verified_bot_developer')
            
        if public_flags.early_supporter:
            badges.append('early_supporter')
            
        if public_flags.active_developer:
            badges.append('active_developer')
        
        # Check Nitro/Boost (premium subscriber)
        if member.premium_since:
            badges.append('boost')
        
        # Check for Nitro (if avatar is animated or custom discriminator)
        if member.display_avatar.is_animated():
            if 'premium' not in badges:
                badges.append('premium')
        
        logger.info(f'Detected badges for {member.name}: {badges}')
        
    except Exception as e:
        logger.error(f'Error detecting badges: {e}')
    
    return badges

def get_badge_description(badge_name):
    """Get human-readable badge description"""
    descriptions = {
        'staff': 'Discord Staff',
        'partner': 'Partnered Server Owner',
        'hypesquad': 'HypeSquad Events',
        'hypesquad_bravery': 'HypeSquad Bravery',
        'hypesquad_brilliance': 'HypeSquad Brilliance',
        'hypesquad_balance': 'HypeSquad Balance',
        'bug_hunter': 'Bug Hunter',
        'bug_hunter_level_2': 'Bug Hunter Level 2',
        'verified_bot_developer': 'Verified Bot Developer',
        'early_supporter': 'Early Supporter',
        'premium': 'Discord Nitro',
        'boost': 'Server Booster',
        'active_developer': 'Active Developer'
    }
    
    return descriptions.get(badge_name, badge_name.replace('_', ' ').title())
