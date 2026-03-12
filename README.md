# 🎉 Advanced Discord Welcome Bot

**Created by SUBHAN DEV (Zero)**

Fully advanced Discord Welcome Bot with custom welcome cards featuring:
- 🖼️ Member banner background
- 👤 Circular profile picture
- 🏅 Discord badges detection
- 📊 Member statistics
- 🎨 Beautiful card design
- ⚡ Zero error system with ultimate error handling

---

## ✨ Features

### 🎨 Welcome Card Features
- **Banner Background**: Uses member's profile banner (if available)
- **Circular Avatar**: Member's profile picture with border
- **Member Info**:
  - Username
  - User ID
  - Member number in server
  - Server join date
  - Account creation date
- **Discord Badges**: Automatically detects and displays:
  - Discord Staff
  - Partner
  - HypeSquad (Bravery, Brilliance, Balance)
  - Bug Hunter (Level 1 & 2)
  - Early Supporter
  - Verified Bot Developer
  - Active Developer
  - Nitro Subscriber
  - Server Booster
- **Beautiful Design**: Gradient backgrounds, shadows, and glowing effects

### 🤖 Bot Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `!help` | Show help menu | Everyone |
| `!ping` | Check bot latency | Everyone |
| `!stats` | Show bot statistics | Everyone |
| `!testwelcome [@member]` | Test welcome card | Admin |
| `!setwelcome [#channel]` | Set welcome channel | Admin |

### 🛡️ Error Handling
- Complete error handling system
- Automatic fallback to text welcome if image fails
- Detailed logging system
- Graceful error recovery
- Permission checks

---

## 🚀 Setup Guide

### 1️⃣ Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Name your bot and click **"Create"**
4. Go to **"Bot"** section in left sidebar
5. Click **"Reset Token"** and copy the token (save it securely!)
6. Scroll down to **"Privileged Gateway Intents"** and enable:
   - ✅ **PRESENCE INTENT**
   - ✅ **SERVER MEMBERS INTENT** (Required!)
   - ✅ **MESSAGE CONTENT INTENT** (Required!)
7. Click **"Save Changes"**

### 2️⃣ Invite Bot to Server

1. Go to **"OAuth2"** > **"URL Generator"**
2. Select scopes:
   - ✅ `bot`
3. Select permissions:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Attach Files
   - ✅ Read Message History
   - ✅ View Channels
4. Copy the generated URL and open it in browser
5. Select your server and authorize

### 3️⃣ Local Setup

```bash
# Clone or download this repository
cd discord-welcome-bot

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env
cp .env.example .env

# Edit .env file and add your bot token
# Use notepad, nano, or any text editor
notepad .env  # Windows
nano .env     # macOS/Linux
```

**Edit `.env` file:**
```env
DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
PREFIX=!
WELCOME_CHANNEL_ID=
LOG_CHANNEL_ID=
```

### 4️⃣ Run Bot Locally

```bash
python bot.py
```

You should see:
```
✅ Bot logged in as YourBot#1234
📊 Connected to X servers
👥 Watching X users
✨ Bot is ready!
```

---

## 🌐 Railway Deployment Guide

### Step 1: Create GitHub Repository

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Advanced Welcome Bot"

# Create repository on GitHub
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/discord-welcome-bot.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Railway

1. Go to [Railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authenticate with GitHub
5. Select your `discord-welcome-bot` repository
6. Click **"Deploy Now"**

### Step 3: Add Environment Variables

1. Go to your project on Railway
2. Click on your deployment
3. Go to **"Variables"** tab
4. Click **"+ New Variable"**
5. Add:
   ```
   Variable Name: DISCORD_TOKEN
   Value: your_bot_token_here
   ```
6. Click **"Add"**
7. Add more variables if needed:
   ```
   PREFIX=!
   WELCOME_CHANNEL_ID=123456789 (optional)
   ```

### Step 4: Deploy

Railway will automatically:
- ✅ Detect Python
- ✅ Install dependencies from `requirements.txt`
- ✅ Run bot using `Procfile`
- ✅ Keep bot online 24/7

Your bot is now **LIVE ON RAILWAY!** 🎉

---

## 📝 Usage Examples

### Test Welcome Card

```
!testwelcome
!testwelcome @username
```

### Set Welcome Channel

```
!setwelcome #welcome
!setwelcome
```

### Check Bot Status

```
!ping
!stats
```

---

## 🎨 Customization

### Change Colors

Edit `config.py`:

```python
BACKGROUND_COLOR = (30, 30, 40)  # Dark background
TEXT_COLOR = (255, 255, 255)     # White text
SECONDARY_COLOR = (150, 150, 150) # Gray text
```

### Change Image Size

```python
IMAGE_WIDTH = 1200
IMAGE_HEIGHT = 400
```

### Change Bot Prefix

In `.env`:
```env
PREFIX=!
```

### Add More Commands

Edit `bot.py` and add:

```python
@bot.command(name='yourcommand')
async def your_command(ctx):
    await ctx.send('Your response!')
```

---

## 🔧 Troubleshooting

### Bot not responding?
- ✅ Check if bot is online (green status)
- ✅ Check if bot has required permissions
- ✅ Check if intents are enabled in Developer Portal
- ✅ Check bot prefix (default is `!`)

### Welcome card not showing?
- ✅ Check if bot has "Attach Files" permission
- ✅ Check if welcome channel is set correctly
- ✅ Check Railway logs for errors

### Badge not showing?
- ✅ Badges only show for users who have them
- ✅ Bot needs "Members Intent" enabled
- ✅ User must have public profile

### Image generation fails?
- ✅ Check Railway logs
- ✅ Pillow library installed correctly
- ✅ Font files available on system

### Railway Deployment Issues?
- ✅ Check if `DISCORD_TOKEN` is set in Variables
- ✅ Check Procfile is correct
- ✅ Check requirements.txt has all dependencies
- ✅ View logs in Railway dashboard

---

## 📋 File Structure

```
discord-welcome-bot/
├── bot.py                    # Main bot file
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── runtime.txt              # Python version
├── Procfile                 # Railway start command
├── .env.example             # Environment template
├── .gitignore               # Git ignore file
├── README.md                # This file
└── utils/
    ├── __init__.py
    ├── image_generator.py    # Welcome card generator
    ├── badge_detector.py     # Badge detection
    └── error_handler.py      # Error handling
```

---

## 🔐 Security

- ⚠️ **NEVER share your bot token publicly!**
- ⚠️ **NEVER commit `.env` file to GitHub!**
- ⚠️ Add `.env` to `.gitignore` (already done)
- ✅ Use environment variables on Railway
- ✅ Keep token in Railway Variables tab only

---

## 📊 Requirements

- Python 3.11+
- discord.py 2.3.2+
- Pillow 10.2.0+
- aiohttp 3.9.3+
- python-dotenv 1.0.0+

---

## 🌟 Features Checklist

- ✅ Advanced welcome cards
- ✅ Banner background support
- ✅ Circular avatar with border
- ✅ Discord badges detection
- ✅ Member statistics
- ✅ Test command for admins
- ✅ Set welcome channel
- ✅ Complete error handling
- ✅ Logging system
- ✅ Railway deployment ready
- ✅ Zero-error architecture
- ✅ Automatic image cleanup
- ✅ Fallback systems
- ✅ Permission checks
- ✅ Help command
- ✅ Stats command

---

## 📞 Support

Created by **SUBHAN DEV (Zero)**

For issues or questions:
1. Check this README thoroughly
2. Check Railway deployment logs
3. Verify all permissions and intents
4. Test locally first before deploying

---

## 📜 License

Free to use and modify for personal projects.
Credit appreciated but not required.

---

## 🎯 Quick Start Checklist

- [ ] Created Discord bot on Developer Portal
- [ ] Enabled all required intents (Members, Presence, Message Content)
- [ ] Copied bot token
- [ ] Invited bot to server
- [ ] Created `.env` file with token
- [ ] Installed dependencies (`pip install -r requirements.txt`)
- [ ] Tested bot locally (`python bot.py`)
- [ ] Created GitHub repository
- [ ] Pushed code to GitHub
- [ ] Created Railway project
- [ ] Connected GitHub repo to Railway
- [ ] Added environment variables on Railway
- [ ] Bot deployed and online! 🎉

---

**Enjoy your advanced Discord Welcome Bot! 🚀**
