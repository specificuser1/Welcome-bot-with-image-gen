import discord
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import aiohttp
import io
import os
from datetime import datetime
import asyncio
from config import *
from utils.badge_detector import get_user_badges
import logging

logger = logging.getLogger('ImageGenerator')

def get_font(size=40):
    """Get font with fallback"""
    for font_path in FONT_PATHS:
        try:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
        except Exception as e:
            logger.debug(f'Failed to load font {font_path}: {e}')
            continue
    
    logger.warning('Using default font')
    return ImageFont.load_default()

async def download_image(url, size=(256, 256)):
    """Download and resize image from URL"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    img = Image.open(io.BytesIO(data))
                    img = img.convert('RGBA')
                    img = img.resize(size, Image.LANCZOS)
                    return img
    except Exception as e:
        logger.error(f'Error downloading image: {e}')
    return None

def create_circular_image(img):
    """Make image circular"""
    try:
        # Create mask
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)
        
        # Apply mask
        output = Image.new('RGBA', img.size, (0, 0, 0, 0))
        output.paste(img, (0, 0))
        output.putalpha(mask)
        
        return output
    except Exception as e:
        logger.error(f'Error creating circular image: {e}')
        return img

def add_glow_effect(img, radius=10):
    """Add glow effect to image"""
    try:
        glow = img.filter(ImageFilter.GaussianBlur(radius))
        output = Image.new('RGBA', img.size, (0, 0, 0, 0))
        output.paste(glow, (0, 0))
        output.paste(img, (0, 0), img)
        return output
    except:
        return img

async def generate_welcome_card(member: discord.Member, guild: discord.Guild):
    """Generate advanced welcome card with banner, avatar, and badges"""
    try:
        logger.info(f'Generating welcome card for {member.name}...')
        
        # Create base image
        img = Image.new('RGBA', (IMAGE_WIDTH, IMAGE_HEIGHT), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)
        
        # === BANNER BACKGROUND (LEFT SIDE) ===
        banner_url = None
        if member.banner:
            banner_url = member.banner.url
        
        if banner_url:
            logger.info(f'Downloading banner for {member.name}...')
            banner = await download_image(banner_url, (400, IMAGE_HEIGHT))
            if banner:
                # Create gradient overlay for banner
                gradient = Image.new('RGBA', (400, IMAGE_HEIGHT), (0, 0, 0, 100))
                img.paste(banner, (0, 0), banner)
                img.paste(gradient, (0, 0), gradient)
        else:
            # Default gradient background for left side
            for i in range(400):
                alpha = int(150 * (1 - i/400))
                color = (50, 50, 80, alpha)
                draw.rectangle([(i, 0), (i+1, IMAGE_HEIGHT)], fill=color)
        
        # === AVATAR (LEFT SIDE, CIRCULAR) ===
        avatar_url = member.display_avatar.url
        logger.info(f'Downloading avatar for {member.name}...')
        avatar = await download_image(avatar_url, (180, 180))
        
        if avatar:
            # Make circular
            avatar = create_circular_image(avatar)
            
            # Add border
            border_img = Image.new('RGBA', (190, 190), (255, 255, 255, 0))
            border_draw = ImageDraw.Draw(border_img)
            border_draw.ellipse((0, 0, 190, 190), outline=(100, 149, 237, 255), width=5)
            
            # Position avatar
            avatar_x = 110
            avatar_y = 110
            img.paste(border_img, (avatar_x - 95, avatar_y - 95), border_img)
            img.paste(avatar, (avatar_x - 90, avatar_y - 90), avatar)
        
        # === CENTER SECTION (MEMBER INFO) ===
        center_x = 450
        center_y = 80
        
        # Member name
        font_large = get_font(50)
        font_medium = get_font(35)
        font_small = get_font(25)
        
        member_name = member.name
        if len(member_name) > 20:
            member_name = member_name[:17] + '...'
        
        # Draw member name with shadow
        shadow_offset = 3
        draw.text((center_x + shadow_offset, center_y + shadow_offset), member_name, 
                 fill=(0, 0, 0, 180), font=font_large)
        draw.text((center_x, center_y), member_name, fill=(255, 255, 255), font=font_large)
        
        # User ID
        center_y += 70
        draw.text((center_x, center_y), f'ID: {member.id}', fill=SECONDARY_COLOR, font=font_small)
        
        # Member count
        center_y += 45
        member_text = f'Member #{guild.member_count:,}'
        draw.text((center_x, center_y), member_text, fill=(100, 200, 100), font=font_medium)
        
        # Join date
        center_y += 50
        join_date = datetime.utcnow().strftime('%d %b %Y')
        draw.text((center_x, center_y), f'Joined: {join_date}', fill=SECONDARY_COLOR, font=font_small)
        
        # Account creation date
        center_y += 40
        created_date = member.created_at.strftime('%d %b %Y')
        draw.text((center_x, center_y), f'Created: {created_date}', fill=SECONDARY_COLOR, font=font_small)
        
        # === BADGES (RIGHT TOP) ===
        badges = get_user_badges(member)
        
        if badges:
            logger.info(f'Found {len(badges)} badges for {member.name}')
            badge_x = IMAGE_WIDTH - 80
            badge_y = 30
            badge_size = 40
            badge_spacing = 50
            
            for i, badge_name in enumerate(badges[:6]):  # Max 6 badges
                if badge_name in BADGE_URLS:
                    badge_img = await download_image(BADGE_URLS[badge_name], (badge_size, badge_size))
                    if badge_img:
                        # Position in grid (2 columns)
                        row = i // 2
                        col = i % 2
                        x = badge_x - (col * badge_spacing)
                        y = badge_y + (row * badge_spacing)
                        img.paste(badge_img, (x, y), badge_img)
        
        # === DECORATIVE ELEMENTS ===
        # Bottom line
        draw.rectangle([(0, IMAGE_HEIGHT - 10), (IMAGE_WIDTH, IMAGE_HEIGHT)], 
                      fill=(100, 149, 237, 200))
        
        # Welcome text at bottom
        welcome_font = get_font(30)
        welcome_text = f'Welcome to {guild.name}!'
        if len(welcome_text) > 40:
            welcome_text = welcome_text[:37] + '...'
        
        # Center the welcome text
        text_bbox = draw.textbbox((0, 0), welcome_text, font=welcome_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (IMAGE_WIDTH - text_width) // 2
        
        draw.text((text_x, IMAGE_HEIGHT - 60), welcome_text, 
                 fill=(255, 255, 255), font=welcome_font)
        
        # Save image
        os.makedirs('temp', exist_ok=True)
        filename = f'temp/welcome_{member.id}_{datetime.utcnow().timestamp()}.png'
        img.save(filename, 'PNG', quality=95)
        
        logger.info(f'✅ Welcome card generated: {filename}')
        return filename
        
    except Exception as e:
        logger.error(f'Error generating welcome card: {e}')
        import traceback
        logger.error(traceback.format_exc())
        return None
