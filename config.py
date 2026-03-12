import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX', '!')
WELCOME_CHANNEL_ID = os.getenv('WELCOME_CHANNEL_ID', None)
LOG_CHANNEL_ID = os.getenv('LOG_CHANNEL_ID', None)

# Image Configuration
IMAGE_WIDTH = 1200
IMAGE_HEIGHT = 400
BACKGROUND_COLOR = (30, 30, 40)
TEXT_COLOR = (255, 255, 255)
SECONDARY_COLOR = (150, 150, 150)

# Font paths (Railway compatible)
FONT_PATHS = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',  # Railway
    '/System/Library/Fonts/Helvetica.ttc',  # macOS
    'C:\\Windows\\Fonts\\arial.ttf',  # Windows
    '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',  # Linux
    './assets/fonts/arial.ttf'  # Local fallback
]

# Badge URLs (Discord CDN)
BADGE_URLS = {
    'staff': 'https://cdn.discordapp.com/badge-icons/5e74e9b61934fc1f67c65515d1f7e60d.png',
    'partner': 'https://cdn.discordapp.com/badge-icons/3f9748e53446a137a052f3454e2de41e.png',
    'hypesquad': 'https://cdn.discordapp.com/badge-icons/bf01d1073931f921909045f3a39fd264.png',
    'hypesquad_bravery': 'https://cdn.discordapp.com/badge-icons/8a88d63823d8a71cd5e390baa45efa02.png',
    'hypesquad_brilliance': 'https://cdn.discordapp.com/badge-icons/011940fd013da3f7fb926e4a1cd2e618.png',
    'hypesquad_balance': 'https://cdn.discordapp.com/badge-icons/3aa41de486fa12454c3761e8e223442e.png',
    'bug_hunter': 'https://cdn.discordapp.com/badge-icons/2717692c7dca7289b35297368a940dd0.png',
    'bug_hunter_level_2': 'https://cdn.discordapp.com/badge-icons/848f79194d4be5ff5f81505cbd0ce1e6.png',
    'verified_bot_developer': 'https://cdn.discordapp.com/badge-icons/6df5892e0f35b051f8b61eace34f4967.png',
    'early_supporter': 'https://cdn.discordapp.com/badge-icons/7060786766c9c840eb3019e725d2b358.png',
    'premium': 'https://cdn.discordapp.com/badge-icons/2ba85e8026a8614b640c2837bcdfe21b.png',
    'boost': 'https://cdn.discordapp.com/badge-icons/ec92202290b48d0879b7413d2dde3bab.png',
    'active_developer': 'https://cdn.discordapp.com/badge-icons/6bdc42827a38498929a4920da12695d9.png'
}

# Validate token
if not TOKEN:
    raise ValueError('❌ DISCORD_TOKEN not found in environment variables! Please set it in .env file')
  
