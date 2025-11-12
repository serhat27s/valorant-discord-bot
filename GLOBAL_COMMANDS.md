# Global Command Synchronization

## ✅ Commands are now GLOBAL

All bot commands are synchronized globally, which means:

### ✨ Advantages:
- ✅ **Works on ALL servers** - Add the bot to any server and commands work
- ✅ **No configuration needed** - No GUILD_ID or server-specific setup required
- ✅ **Single source of truth** - All servers have the same commands
- ✅ **Easy to scale** - Perfect for public bots

### ⏱️ Important Notes:
- **Initial sync takes up to 1 hour** after bot start
- Commands appear automatically on all servers where the bot is present
- No need to restart the bot when adding to new servers
- Once synced, commands are instant on all servers

## 🚀 First Time Setup:

1. Start the bot: `py bot.py`
2. You'll see: `✅ Synced 6 command(s) globally`
3. Wait up to 1 hour for Discord to propagate commands
4. Commands will appear on all servers where the bot is present

## 🔄 After Commands are Live:

Once the initial sync is complete:
- Commands are **instantly available** on any new server you add the bot to
- No waiting period for new servers
- Updates to commands still take up to 1 hour to propagate

## 📋 Available Commands:

1. `/linkacc` - Link Valorant account
2. `/unlinkacc` - Unlink account
3. `/stats` - View player stats
4. `/matches` - View match history
5. `/rank` - View rank & RR
6. `/leaderboard` - Server leaderboard

## 💡 Troubleshooting:

**Commands not showing up?**
- Wait the full hour after first bot start
- Refresh Discord (Ctrl + R)
- Check bot permissions (requires "applications.commands" scope)

**Commands showing duplicates?**
- Old guild-specific commands may exist from previous setup
- They will auto-remove within 1 hour after bot restart
- Or manually remove them in Discord Server Settings → Integrations

## 🔧 Technical Details:

```python
# The bot uses simple global sync:
@bot.event
async def on_ready():
    synced = await bot.tree.sync()  # Global sync
    print(f'✅ Synced {len(synced)} command(s) globally')
```

No GUILD_ID needed, no server-specific logic!

