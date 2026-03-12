#!/usr/bin/env python3
"""
Test Script for Discord Welcome Bot
Created by SUBHAN DEV (Zero)
"""

import os
import sys

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...\n")
    
    errors = []
    warnings = []
    
    # Check Python version
    print("📋 Python Version:", sys.version)
    if sys.version_info < (3, 11):
        warnings.append("Python 3.11+ recommended for best compatibility")
    else:
        print("✅ Python version OK\n")
    
    # Check if .env exists
    if not os.path.exists('.env'):
        errors.append(".env file not found! Copy .env.example to .env and add your bot token")
    else:
        print("✅ .env file exists\n")
        
        # Check if token is set
        from dotenv import load_dotenv
        load_dotenv()
        
        token = os.getenv('DISCORD_TOKEN')
        if not token or token == 'your_bot_token_here':
            errors.append("DISCORD_TOKEN not set in .env file!")
        else:
            print("✅ Discord token found\n")
    
    # Check dependencies
    print("📦 Checking dependencies...\n")
    
    try:
        import discord
        print(f"✅ discord.py version: {discord.__version__}")
    except ImportError:
        errors.append("discord.py not installed! Run: pip install -r requirements.txt")
    
    try:
        from PIL import Image
        print(f"✅ Pillow installed")
    except ImportError:
        errors.append("Pillow not installed! Run: pip install -r requirements.txt")
    
    try:
        import aiohttp
        print(f"✅ aiohttp installed")
    except ImportError:
        errors.append("aiohttp not installed! Run: pip install -r requirements.txt")
    
    try:
        import dotenv
        print(f"✅ python-dotenv installed")
    except ImportError:
        errors.append("python-dotenv not installed! Run: pip install -r requirements.txt")
    
    print()
    
    # Check file structure
    print("📁 Checking file structure...\n")
    
    required_files = [
        'bot.py',
        'config.py',
        'requirements.txt',
        'Procfile',
        'utils/__init__.py',
        'utils/image_generator.py',
        'utils/badge_detector.py',
        'utils/error_handler.py'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            errors.append(f"Missing file: {file}")
    
    print()
    
    # Report results
    print("=" * 50)
    
    if errors:
        print("❌ ERRORS FOUND:\n")
        for error in errors:
            print(f"  ❌ {error}")
        print()
    
    if warnings:
        print("⚠️  WARNINGS:\n")
        for warning in warnings:
            print(f"  ⚠️  {warning}")
        print()
    
    if not errors and not warnings:
        print("✅ ALL CHECKS PASSED!\n")
        print("You can now run the bot with: python bot.py")
    elif not errors:
        print("✅ All required checks passed!")
        print("⚠️  Some warnings exist, but bot should work")
        print("\nYou can run the bot with: python bot.py")
    else:
        print("❌ Please fix the errors above before running the bot")
        return False
    
    print("=" * 50)
    return True

if __name__ == '__main__':
    print("=" * 50)
    print("Discord Welcome Bot - Test Script")
    print("Created by SUBHAN DEV (Zero)")
    print("=" * 50)
    print()
    
    success = check_requirements()
    
    sys.exit(0 if success else 1)
