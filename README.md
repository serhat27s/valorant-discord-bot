# 🎮 Valorant Discord Bot

A feature-rich Discord bot that provides comprehensive Valorant statistics and leaderboards using the Henrik Dev API. Track your competitive performance, view detailed match history, and compete with your server members!

[![Discord.py](https://img.shields.io/badge/discord.py-2.3.0+-blue.svg)](https://github.com/Rapptz/discord.py)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ Features

- **📊 Detailed Player Statistics** - View comprehensive stats from recent competitive matches
- **🏆 Server Leaderboards** - Compete with other players on your Discord server
- **🔗 Account Linking** - Link your Valorant account for easier access to your stats
- **📈 Rank Tracking** - Monitor your current rank, RR, and peak rank
- **🎯 Match History** - Review your last 10 competitive matches with detailed breakdowns
- **🌍 Multi-Region Support** - Works across EU, NA, AP, and KR regions
- **🎨 Rich Embeds** - Beautiful Discord embeds with rank-colored themes

---

## 🤖 Add Bot to Your Server

Want to use this bot without hosting it yourself? Click the link below to invite it to your server!

[![Add to Discord](https://img.shields.io/badge/Add%20to%20Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](YOUR_INVITE_LINK_HERE)

> **� Note:** Replace `YOUR_INVITE_LINK_HERE` with your actual bot invite link. You can generate one from the [Discord Developer Portal](https://discord.com/developers/applications) → Your App → OAuth2 → URL Generator.

---

## �📋 Commands

### 🔗 Account Management
| Command | Description |
|---------|-------------|
| `/linkacc <name> <tag> [region]` | Link your Valorant account to avoid entering credentials each time |
| `/unlinkacc` | Remove your linked Valorant account |

### 📊 Player Stats
| Command | Description | Parameters |
|---------|-------------|------------|
| `/stats [name] [tag] [region]` | Show overview stats from last 10 ranked matches | Optional if account is linked |
| `/matches [name] [tag] [region]` | Display last 10 ranked matches with detailed stats | Optional if account is linked |
| `/rank [name] [tag] [region]` | Show current rank, RR, and peak rank with MMR tracking | Optional if account is linked |

### 🏆 Server Features
| Command | Description |
|---------|-------------|
| `/leaderboard` | Display server-wide leaderboard of all linked accounts |

## � Usage Examples

### Linking Your Account
```
/linkacc name:PlayerName tag:1234 region:eu
```
After linking, you can use all stat commands without parameters!

### Viewing Stats
```
/stats
```
Shows:
- Average Damage per Round (ADR)
- Kill/Death/Assist (KDA) ratio
- Headshot percentage
- Win rate
- Total kills/deaths/assists

### Checking Match History
```
/matches
```
Displays your last 10 competitive matches with:
- Map and agent played
- Score and result (Win/Loss)
- Individual performance (K/D/A)
- RR change
- Headshot percentage

### Server Leaderboard
```
/leaderboard
```
Shows all linked accounts ranked by:
- Current rank tier
- Ranked Rating (RR)
- Player name and tag

## 🌍 Supported Regions

| Region Code | Region Name |
|-------------|-------------|
| `eu` | Europe (Default) |
| `na` | North America |
| `ap` | Asia-Pacific |
| `kr` | Korea |

---

# 🖥️ Self-Hosting Guide

Want to run your own instance of this bot? Follow the guide below!

## Prerequisites

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **Discord Bot Token** - [Discord Developer Portal](https://discord.com/developers/applications)
- **Henrik Dev API Key** - [Get API Key](https://docs.henrikdev.xyz/)
- **Git** (optional) - For cloning the repository

## Step 1: Create a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"** and give it a name
3. Go to the **"Bot"** tab and click **"Add Bot"**
4. Under the bot's username, click **"Reset Token"** and copy your token
5. Enable the following **Privileged Gateway Intents**:
   - ✅ Message Content Intent
6. Save your changes

## Step 2: Generate Bot Invite Link

1. In the Developer Portal, go to **OAuth2 → URL Generator**
2. Select the following **Scopes**:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Select the following **Bot Permissions**:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Message History
   - ✅ Use Slash Commands
4. Copy the generated URL and use it to invite the bot to your server

## Step 3: Get Henrik Dev API Key

1. Go to [Henrik Dev API](https://docs.henrikdev.xyz/)
2. Create an account or sign in
3. Generate an API key from your dashboard
4. Keep this key safe - you'll need it for configuration

## Step 4: Download & Install

### Option A: Clone with Git
```bash
git clone https://github.com/yourusername/Valorant-Discord_bot.git
cd Valorant-Discord_bot
```

### Option B: Download ZIP
1. Download the repository as a ZIP file
2. Extract it to your desired location
3. Open a terminal in the extracted folder

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 5: Configure Environment Variables

Create a `.env` file in the root directory:

```env
DISCORD_TOKEN=your_discord_bot_token_here
VALORANT_API_KEY=your_henrikdev_api_key_here
```

> ⚠️ **Important:** Never share your `.env` file or commit it to GitHub!

## Step 6: Run the Bot

```bash
python bot.py
```

You should see output similar to:
```
Logged in as YourBotName#1234
✅ Synced 6 command(s) globally
```

> **Note:** Global command sync takes up to **1 hour** on first run. After that, commands are available instantly on all servers.

---

## 🔧 Advanced Configuration

### Running as a Background Service (Windows)

1. Create a batch file `start_bot.bat`:
   ```batch
   @echo off
   cd /d "C:\path\to\Valorant-Discord_bot"
   python bot.py
   pause
   ```

2. Use Task Scheduler to run the batch file on startup

### Running as a Background Service (Linux)

1. Create a systemd service file `/etc/systemd/system/valorant-bot.service`:
   ```ini
   [Unit]
   Description=Valorant Discord Bot
   After=network.target

   [Service]
   Type=simple
   User=your_username
   WorkingDirectory=/path/to/Valorant-Discord_bot
   ExecStart=/usr/bin/python3 bot.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

2. Enable and start the service:
   ```bash
   sudo systemctl enable valorant-bot
   sudo systemctl start valorant-bot
   ```

### Running with Docker (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "bot.py"]
```

Build and run:
```bash
docker build -t valorant-bot .
docker run -d --env-file .env valorant-bot
```

---

## 🐛 Troubleshooting

### Commands Not Showing Up

| Problem | Solution |
|---------|----------|
| Commands don't appear after starting bot | Wait up to 1 hour for global sync to complete |
| Commands still missing after 1 hour | Refresh Discord with `Ctrl + R` |
| Commands only missing on specific server | Check bot has `applications.commands` scope when invited |
| Duplicate commands appearing | Old guild commands may exist - they auto-remove within 1 hour |

### Bot Won't Start

| Problem | Solution |
|---------|----------|
| `DISCORD_TOKEN not found` | Make sure `.env` file exists and contains your token |
| `Invalid token` | Regenerate your bot token in Discord Developer Portal |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Python not recognized | Add Python to your system PATH or use `py` instead of `python` |

### API Errors

| Problem | Solution |
|---------|----------|
| `401 Unauthorized` | Check your Henrik Dev API key is correct |
| `429 Too Many Requests` | You've hit the rate limit - wait a few minutes |
| `Player not found` | Verify the Riot ID (name#tag) is correct and case-sensitive |
| `No matches found` | Player may not have recent competitive matches |

### Account Linking Issues

| Problem | Solution |
|---------|----------|
| Linked account not working | Make sure you used the correct region when linking |
| Stats showing wrong account | Unlink (`/unlinkacc`) and relink with correct details |
| `linked_accounts.json` corrupted | Delete the file - it will be recreated |

### Connection Issues

| Problem | Solution |
|---------|----------|
| Bot keeps disconnecting | Check your internet connection |
| `Cannot connect to Discord` | Discord may be experiencing outages - check [Discord Status](https://discordstatus.com/) |
| Timeouts on API calls | Henrik Dev API may be slow - commands will retry automatically |

---

## 📁 Project Structure

```
Valorant-Discord_bot/
├── bot.py                 # Main bot logic and Discord commands
├── valorant_api.py        # Valorant API wrapper and data processing
├── requirements.txt       # Python dependencies
├── linked_accounts.json   # Linked account storage (auto-generated)
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🛠️ Technologies Used

- **[Discord.py](https://github.com/Rapptz/discord.py)** - Discord API wrapper
- **[Henrik Dev Valorant API](https://docs.henrikdev.xyz/)** - Valorant statistics and data
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** - Environment variable management
- **[Requests](https://docs.python-requests.org/)** - HTTP library for API calls

## 🔒 Data Storage

The bot stores linked accounts locally in `linked_accounts.json`. This file contains:
- Discord User IDs
- Linked Valorant names and tags
- Preferred regions

> **Privacy Note:** Account data is stored locally and never shared with third parties.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Credits

- Valorant statistics powered by [Henrik Dev API](https://docs.henrikdev.xyz/)
- Built with [Discord.py](https://github.com/Rapptz/discord.py)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/Valorant-Discord_bot/issues).

## 📬 Support

If you have any questions or need help, please open an issue on GitHub.

---

**Made with ❤️ for the Valorant community**
