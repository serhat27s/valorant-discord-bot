import discord
from discord.ext import commands
from discord import app_commands
import os
import json
from dotenv import load_dotenv
from valorant_api import ValorantAPI

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Initialize Valorant API
valorant_api = ValorantAPI(os.getenv('VALORANT_API_KEY'))

# Default region (can be changed)
DEFAULT_REGION = "eu"

def get_rank_color(tier: int) -> int:
    if tier >= 27:  # Radiant
        return 0xFFFF85  # Bright yellow/gold
    elif tier >= 24:  # Immortal
        return 0xBB3D6B  # Red/Pink
    elif tier >= 21:  # Ascendant
        return 0x1EBC61  # Green
    elif tier >= 18:  # Diamond
        return 0xB489D5  # Purple
    elif tier >= 15:  # Platinum
        return 0x59A7B3  # Cyan
    elif tier >= 12:  # Gold
        return 0xF0B232  # Gold
    elif tier >= 9:   # Silver
        return 0xCCD1D1  # Silver/Gray
    elif tier >= 6:   # Bronze
        return 0xA87854  # Brown
    elif tier >= 3:   # Iron
        return 0x4D4D4D  # Dark gray
    else:  # Unranked
        return 0x5865F2  # Discord blue

# Account linking functions
LINKED_ACCOUNTS_FILE = "linked_accounts.json"

def load_linked_accounts():
    #""Load linked accounts from JSON file""
    try:
        if os.path.exists(LINKED_ACCOUNTS_FILE):
            with open(LINKED_ACCOUNTS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading linked accounts: {e}")
    return {}

def save_linked_accounts(accounts):
    #""Save linked accounts to JSON file""
    try:
        with open(LINKED_ACCOUNTS_FILE, 'w') as f:
            json.dump(accounts, f, indent=2)
    except Exception as e:
        print(f"Error saving linked accounts: {e}")

def get_linked_account(user_id):
    """Get linked account for a Discord user"""
    accounts = load_linked_accounts()
    return accounts.get(str(user_id))

def link_account(user_id, name, tag, region):
    #""Link a Valorant account to a Discord user""
    accounts = load_linked_accounts()
    accounts[str(user_id)] = {
        "name": name,
        "tag": tag,
        "region": region
    }
    save_linked_accounts(accounts)

@bot.event
async def on_ready():
    print(f'{bot.user} is now online!')
    try:
        # Server-specific sync for instant availability
        YOUR_GUILD_ID = 815990361800441906
        guild = discord.Object(id=YOUR_GUILD_ID)

        # Sync to your specific server (instant)
        bot.tree.copy_global_to(guild=guild)
        synced_guild = await bot.tree.sync(guild=guild)
        # Global synchronization - commands available on all servers
        synced = await bot.tree.sync()
        print(f'✅ Synced {len(synced)} command(s) globally')
        print(f'⏱️  Commands will be available in all servers within 1 hour')
    except Exception as e:
        print(f'❌ Error syncing commands: {e}')

@bot.tree.command(name="help", description="Shows all available commands with descriptions")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📖 Valorant Stats Bot - Commands",
        description="All available commands and their descriptions",
        color=0x5865F2
    )

    # Account Management Section
    embed.add_field(
        name="🔗 Account Management",
        value=(
            "**`/linkacc`** - Link your Valorant account\n"
            "└ Use commands without entering name/tag every time\n\n"
            "**`/unlinkacc`** - Unlink your Valorant account\n"
            "└ Remove the linked account from your profile"
        ),
        inline=False
    )

    # Player Stats Section
    embed.add_field(
        name="📊 Player Statistics",
        value=(
            "**`/stats`** - Player performance overview\n"
            "└ K/D, ADR, DDΔ, HS%, Winrate from last 10 matches\n\n"
            "**`/matches`** - Match history (last 10 games)\n"
            "└ Detailed stats, agent icons, map images, RR changes\n\n"
            "**`/rank`** - Current rank & peak rank\n"
            "└ Shows rank, RR, MMR changes, and peak season"
        ),
        inline=False
    )

    # Server Features Section
    embed.add_field(
        name="🏆 Server Features",
        value=(
            "**`/leaderboard`** - Server ranked leaderboard\n"
            "└ Top 15 players sorted by rank and RR\n\n"
            "**`/help`** - Shows this help message\n"
            "└ Overview of all commands"
        ),
        inline=False
    )

    # Quick Tips
    embed.add_field(
        name="💡 Quick Tips",
        value=(
            "• Link your account with `/linkacc` to use all commands without parameters\n"
            "• All commands support EU, NA, AP, KR regions\n"
            "• Use `/leaderboard` to compete with friends on your server"
        ),
        inline=False
    )

    embed.set_footer(
        text=f"Requested by {interaction.user.name} | Powered by Henrik Dev API",
        icon_url=interaction.user.display_avatar.url
    )
    embed.timestamp = discord.utils.utcnow()

    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="linkacc", description="Link your Valorant account to use commands without entering name/tag")
@app_commands.describe(
    name="Riot ID Name (e.g., Player)",
    tag="Riot ID Tag (e.g., EUW)",
    region="Region (eu, na, ap, kr) - optional, defaults to EU"
)
async def linkacc(interaction: discord.Interaction, name: str, tag: str, region: str = None):
    try:
        # Use default region if not specified
        if not region:
            region = DEFAULT_REGION

        # Verify account exists
        account_data = valorant_api.get_account(name, tag)

        if not account_data or account_data.get("status") != 200:
            await interaction.response.send_message(
                f"❌ Account **{name}#{tag}** not found. Please check the name and tag.",
                ephemeral=True
            )
            return

        # Link the account
        link_account(interaction.user.id, name, tag, region)

        embed = discord.Embed(
            title="✅ Account Linked Successfully!",
            description=f"Your Discord account has been linked to **{name}#{tag}**",
            color=0x00D26A
        )

        embed.add_field(
            name="📝 Linked Account",
            value=f"**Name:** {name}\n**Tag:** #{tag}\n**Region:** {region.upper()}",
            inline=False
        )

        embed.add_field(
            name="💡 How to use",
            value="You can now use `/stats`, `/matches`, and `/rank` without entering your name and tag!",
            inline=False
        )

        embed.set_footer(text=f"Linked by {interaction.user.name}")
        embed.timestamp = discord.utils.utcnow()

        await interaction.response.send_message(embed=embed, ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(
            f"❌ Error linking account: {str(e)}",
            ephemeral=True
        )

@bot.tree.command(name="unlinkacc", description="Unlink your Valorant account")
async def unlinkacc(interaction: discord.Interaction):
    try:
        # Check if account is linked
        linked = get_linked_account(interaction.user.id)

        if not linked:
            await interaction.response.send_message(
                "❌ No account linked! Use `/linkacc` to link an account first.",
                ephemeral=True
            )
            return

        # Remove the linked account
        accounts = load_linked_accounts()
        del accounts[str(interaction.user.id)]
        save_linked_accounts(accounts)

        embed = discord.Embed(
            title="✅ Account Unlinked Successfully!",
            description=f"Your Discord account has been unlinked from **{linked['name']}#{linked['tag']}**",
            color=0xFD4556
        )

        embed.add_field(
            name="💡 What's next?",
            value="You'll need to provide name and tag when using commands, or link a new account with `/linkacc`.",
            inline=False
        )

        embed.set_footer(text=f"Unlinked by {interaction.user.name}")
        embed.timestamp = discord.utils.utcnow()

        await interaction.response.send_message(embed=embed, ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(
            f"❌ Error unlinking account: {str(e)}",
            ephemeral=True
        )

@bot.tree.command(name="stats", description="Shows an overview of stats from the last 10 Ranked matches")
@app_commands.describe(
    name="Riot ID Name (optional if account is linked)",
    tag="Riot ID Tag (optional if account is linked)",
    region="Region (eu, na, ap, kr)"
)
async def stats(interaction: discord.Interaction, name: str = None, tag: str = None, region: str = None):
    await interaction.response.defer()

    try:
        # Check for linked account if name/tag not provided
        if not name or not tag:
            linked = get_linked_account(interaction.user.id)
            if linked:
                name = name or linked.get("name")
                tag = tag or linked.get("tag")
                region = region or linked.get("region", DEFAULT_REGION)
            else:
                await interaction.followup.send(
                    "❌ No account linked! Use `/linkacc` to link your account or provide name and tag.",
                    ephemeral=True
                )
                return

        # Use default region if not specified
        if not region:
            region = DEFAULT_REGION
        # Get account information for playercard
        print(f"DEBUG: Fetching account for {name}#{tag}")
        account_data = valorant_api.get_account(name, tag)

        if not account_data:
            await interaction.followup.send(f"❌ Account **{name}#{tag}** not found.\n*Tip: Pay attention to capitalization and correct spelling.*")
            return

        if account_data.get("status") != 200:
            error_msg = account_data.get("errors", [{}])[0].get("message", "Unknown error")
            await interaction.followup.send(f"❌ Error retrieving account information: {error_msg}")
            return

        # Get MMR data for rank icon
        mmr_data = valorant_api.get_mmr(region, name, tag)

        # Get last 10 matches from current act
        print(f"DEBUG: Fetching matches for {name}#{tag} in region {region}")

        act_matches = valorant_api.get_all_act_matches(region, name, tag, mode="competitive")

        if not act_matches:
            await interaction.followup.send(f"❌ Player **{name}#{tag}** not found or no data available.")
            return

        if act_matches.get("status") != 200:
            await interaction.followup.send(f"❌ Error retrieving data.")
            return

        total_in_act = len(act_matches.get("data", [])) if act_matches else 0
        print(f"DEBUG: Retrieved {total_in_act} matches from current act for {name}#{tag}")

        if not act_matches.get("data"):
            await interaction.followup.send(f"❌ No matches in current act found for **{name}#{tag}**.")
            return

        # Calculate stats from the 10 matches
        stats_data = valorant_api.calculate_stats(act_matches, name, tag)

        if not stats_data:
            await interaction.followup.send(f"❌ No statistics found for **{name}#{tag}**.")
            return

        total_matches = stats_data.get('matches', 0)
        print(f"DEBUG: Calculated stats from {total_matches} matches")

        # Get current act name from MMR API (more reliable)
        current_act = valorant_api.get_current_season_name(region, name, tag)

        # Create embed with card-style layout
        embed = discord.Embed(
            title=f"**{name}#{tag}** • **{current_act}**",
            description=f"📊 Stats overview last ** 10 matches **in ranked",
            color=0x5865F2  # discord color
        )

        embed.add_field(
            name="💀 Kills",
            value=f"```{stats_data['kills']}```",
            inline=True
        )

        embed.add_field(
            name="📊 K/D Ratio",
            value=f"```{round(stats_data['kills'] / max(stats_data['deaths'], 1), 2)}```",
            inline=True
        )

        embed.add_field(name="\u200b", value="\u200b", inline=True)  # Spacer
        # Main stats section
        embed.add_field(
            name="🎯 Headshot %",
            value=f"```{stats_data['hs_percentage']}%```",
            inline=True
        )

        embed.add_field(
            name="🏆 Winrate",
            value=f"```{stats_data['winrate']}%```",
            inline=True
        )

        embed.add_field(name="\u200b", value="\u200b", inline=True)

        embed.add_field(
            name="💥 ADR/Round",
            value=f"```{stats_data['avg_damage']}```",
            inline=True
        )

        damage_delta = stats_data.get('damage_delta', 0)
        delta_sign = "+" if damage_delta >= 0 else ""
        embed.add_field(
            name="Δ DDΔ/Round",
            value=f"```{delta_sign}{damage_delta}```",
            inline=True
        )

        embed.add_field(name="\u200b", value="\u200b", inline=True)

        #Rank icon
        rank_icon_url = "https://i.imgur.com/JkNS0Xu.png"  # Default Valorant logo
        if mmr_data and mmr_data.get("status") == 200:
            current_data = mmr_data.get("data", {}).get("current_data", {})
            rank_icon = current_data.get("images", {}).get("small")
            if rank_icon:
                rank_icon_url = rank_icon

        embed.set_thumbnail(url=rank_icon_url)

        # Add playercard as image if available
        if account_data and account_data.get("status") == 200:
            card_data = account_data.get("data", {}).get("card", {})
            playercard_url = card_data.get("wide") or card_data.get("large")
            if playercard_url:
                embed.set_image(url=playercard_url)

        # Footer
        embed.set_footer(
            text=f"Stats from the last {total_matches} matches in {current_act}",
            icon_url=interaction.user.display_avatar.url
        )

        embed.timestamp = discord.utils.utcnow()

        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(f"❌ Error retrieving statistics: {str(e)}")

@bot.tree.command(name="matches", description="Shows the last 10 ranked matches with detailed stats")
@app_commands.describe(
    name="Riot ID Name (optional if account is linked)",
    tag="Riot ID Tag (optional if account is linked)",
    region="Region (eu, na, ap, kr)"
)
async def matches(interaction: discord.Interaction, name: str = None, tag: str = None, region: str = None):
    await interaction.response.defer()

    try:
        # Check for linked account if name/tag not provided
        if not name or not tag:
            linked = get_linked_account(interaction.user.id)
            if linked:
                name = name or linked.get("name")
                tag = tag or linked.get("tag")
                region = region or linked.get("region", DEFAULT_REGION)
            else:
                await interaction.followup.send(
                    "❌ No account linked! Use `/linkacc` to link your account or provide name and tag.",
                    ephemeral=True
                )
                return

        # Use default region if not specified
        if not region:
            region = DEFAULT_REGION
        # Get last 10 matches from current act
        act_matches = valorant_api.get_all_act_matches(region, name, tag, mode="competitive")

        if not act_matches or act_matches.get("status") != 200:
            await interaction.followup.send(f"❌ No matches found for **{name}#{tag}**.")
            return

        if not act_matches.get("data"):
            await interaction.followup.send(f"❌ No matches found in current act for **{name}#{tag}**.")
            return

        # Get MMR History for RR changes
        import requests
        mmr_history_url = f"{valorant_api.base_url}/v1/mmr-history/{region}/{name}/{tag}"
        mmr_response = requests.get(mmr_history_url, headers=valorant_api.headers)

        rr_changes_map = {}  # Map match_id to RR change
        if mmr_response.status_code == 200:
            mmr_history_data = mmr_response.json()
            if mmr_history_data.get("status") == 200:
                history = mmr_history_data.get("data", [])
                for match in history:
                    match_id = match.get("match_id")
                    rr_change = match.get("mmr_change_to_last_game", 0)
                    if match_id:
                        rr_changes_map[match_id] = rr_change

        # Limit to 10 matches (Discord allows max 10 embeds per message)
        matches_to_show = act_matches["data"][:10]

        # Create list of embeds - one per match
        embeds = []

        for idx, match in enumerate(matches_to_show, 1):
            # Find player in match
            player_stats = None
            players = match.get("players", {}).get("all_players", [])
            for player in players:
                if player.get("name", "").lower() == name.lower() and player.get("tag", "").lower() == tag.lower():
                    player_stats = player
                    break

            if not player_stats:
                continue

            # Determine if won
            team = player_stats.get("team", "").lower()
            won = False
            red_rounds = match.get("teams", {}).get("red", {}).get("rounds_won", 0)
            blue_rounds = match.get("teams", {}).get("blue", {}).get("rounds_won", 0)

            if team == "red":
                won = match.get("teams", {}).get("red", {}).get("has_won", False)
                player_score = f"{red_rounds}-{blue_rounds}"
            else:
                won = match.get("teams", {}).get("blue", {}).get("has_won", False)
                player_score = f"{blue_rounds}-{red_rounds}"

            # Result text and color
            result_text = f"Win {player_score}" if won else f"Loss {player_score}"
            embed_color = 0x00D26A if won else 0xFD4556  # Green for win, Red for loss

            # Get match date and convert time to 24-hour format
            from datetime import datetime
            import re

            match_date = match.get("metadata", {}).get("game_start_patched", "Unknown date")

            # Convert to 24h format
            if match_date != "Unknown date":
                try:
                    # Find the time portion (e.g., "6:28 PM")
                    time_match = re.search(r'(\d{1,2}):(\d{2})\s*([AP]M)', match_date)
                    if time_match:
                        hour = int(time_match.group(1))
                        minute = time_match.group(2)
                        period = time_match.group(3)

                        # Convert to 24-hour format
                        if period == "PM" and hour != 12:
                            hour += 12
                        elif period == "AM" and hour == 12:
                            hour = 0

                        time_24h = f"{hour:02d}:{minute}"
                        match_date = re.sub(r'\d{1,2}:\d{2}\s*[AP]M', time_24h, match_date)
                except:
                    pass  # Keep original if conversion fails

            # Map and agent
            map_name = match.get("metadata", {}).get("map", "Unknown")
            agent = player_stats.get("character", "Unknown")

            # Calculate stats
            stats = player_stats.get("stats", {})
            kills = stats.get("kills", 0)
            deaths = stats.get("deaths", 0)
            assists = stats.get("assists", 0)

            # Calculate headshot percentage for this match
            headshots = stats.get("headshots", 0)
            bodyshots = stats.get("bodyshots", 0)
            legshots = stats.get("legshots", 0)
            total_shots = headshots + bodyshots + legshots
            hs_percent = round((headshots / max(total_shots, 1)) * 100, 1)

            # Get lobby placement (leaderboard position based on score)
            # Sort all players by score to find placement
            all_players = match.get("players", {}).get("all_players", [])
            sorted_players = sorted(all_players, key=lambda p: p.get("stats", {}).get("score", 0), reverse=True)
            lobby_placement = 1
            for i, p in enumerate(sorted_players, 1):
                if p.get("name", "").lower() == name.lower() and p.get("tag", "").lower() == tag.lower():
                    lobby_placement = i
                    break

            # Get agent icon
            agent_icon_url = player_stats.get("assets", {}).get("agent", {}).get("small")

            # Get map image - construct URL from map name
            # Valorant API map images format
            map_images = {
                "Abyss": "https://media.valorant-api.com/maps/224b0a95-48b9-f703-1bd8-67aca101a61f/splash.png",
                "Ascent": "https://media.valorant-api.com/maps/7eaecc1b-4337-bbf6-6ab9-04b8f06b3319/splash.png",
                "Bind": "https://media.valorant-api.com/maps/2c9d57ec-4431-9c5e-2939-8f9ef6dd5cba/splash.png",
                "Breeze": "https://media.valorant-api.com/maps/2fb9a4fd-47b8-4e7d-a969-74b4046ebd53/splash.png",
                "Fracture": "https://media.valorant-api.com/maps/b529448b-4d60-346e-e89e-00a4c527a405/splash.png",
                "Haven": "https://media.valorant-api.com/maps/2bee0dc9-4ffe-519b-1cbd-7fbe763a6047/splash.png",
                "Icebox": "https://media.valorant-api.com/maps/e2ad5c54-4114-a870-9641-8ea21279579a/splash.png",
                "Lotus": "https://media.valorant-api.com/maps/2fe4ed3a-450a-948b-6d6b-e89a78e680a9/splash.png",
                "Pearl": "https://media.valorant-api.com/maps/fd267378-4d1d-484f-ff52-77821ed10dc2/splash.png",
                "Split": "https://media.valorant-api.com/maps/d960549e-485c-e861-8d71-aa9d1aed12a2/splash.png",
                "Sunset": "https://media.valorant-api.com/maps/92584fbe-486a-b1b2-9faa-39b0f486b498/splash.png",
                "Corrode": "https://media.valorant-api.com/maps/1c18ab1f-420d-0d8b-71d0-77ad3c439115/splash.png"
            }
            map_image_url = map_images.get(map_name)

            # Create embed for this match
            match_embed = discord.Embed(
                title=f"🎮 {result_text}",
                color=embed_color
            )

            # Set agent icon as thumbnail (oben rechts)
            if agent_icon_url:
                match_embed.set_thumbnail(url=agent_icon_url)

            # Set map image as large image (unten, groß)
            if map_image_url:
                match_embed.set_image(url=map_image_url)

            match_embed.add_field(
                name="📊 K/D/A",
                value=f"**{kills}/{deaths}/{assists}**",
                inline=True
            )

            match_embed.add_field(
                name="🎯 Headshot %",
                value=f"**{hs_percent}%**",
                inline=True
            )

            match_embed.add_field(name="\u200b", value="\u200b", inline=True)

            match_embed.add_field(
                name="🏅 Placement",
                value=f"**#{lobby_placement}**/10",
                inline=True
            )

            # Get RR change for this match
            match_id = match.get("metadata", {}).get("matchid")
            rr_change = rr_changes_map.get(match_id, None)

            if rr_change is not None:
                rr_sign = "+" if rr_change >= 0 else ""
                rr_color = "🟢" if rr_change >= 0 else "🔴"
                match_embed.add_field(
                    name="📈 RR Change",
                    value=f"**{rr_color} {rr_sign}{rr_change}**",
                    inline=True
                )

            match_embed.add_field(name="\u200b", value="\u200b", inline=True)

            match_embed.set_footer(text=f"{match_date}")

            embeds.append(match_embed)

        # Send all embeds at once (max 10)
        if embeds:
            await interaction.followup.send(embeds=embeds)
        else:
            await interaction.followup.send(f"❌ No match data found for **{name}#{tag}**.")

    except Exception as e:
        await interaction.followup.send(f"❌ Error retrieving matches: {str(e)}")

@bot.tree.command(name="leaderboard", description="Shows a leaderboard of all linked accounts sorted by rank")
async def leaderboard(interaction: discord.Interaction):
    await interaction.response.defer()

    try:
        # Load all linked accounts
        accounts = load_linked_accounts()

        if not accounts:
            await interaction.followup.send(
                "❌ No linked accounts found! Users need to link their accounts with `/linkacc` first.",
                ephemeral=True
            )
            return

        # Fetch rank data for all linked accounts
        leaderboard_data = []

        for user_id, account_info in accounts.items():
            name = account_info.get("name")
            tag = account_info.get("tag")
            region = account_info.get("region", DEFAULT_REGION)

            try:
                # Get Discord user
                user = await bot.fetch_user(int(user_id))
                discord_name = user.name if user else "Unknown"

                # Get MMR data
                mmr_data = valorant_api.get_mmr(region, name, tag)

                if mmr_data and mmr_data.get("status") == 200:
                    current_data = mmr_data.get("data", {}).get("current_data", {})

                    tier = current_data.get("currenttier", 0)
                    rank = current_data.get("currenttierpatched", "Unranked")
                    rr = current_data.get("ranking_in_tier", 0)
                    elo = current_data.get("elo", 0)

                    leaderboard_data.append({
                        "discord_name": discord_name,
                        "valorant_name": f"{name}#{tag}",
                        "tier": tier,
                        "rank": rank,
                        "rr": rr,
                        "elo": elo
                    })
            except Exception as e:
                print(f"Error fetching data for {name}#{tag}: {e}")
                continue

        if not leaderboard_data:
            await interaction.followup.send(
                "❌ Could not fetch rank data for any linked accounts.",
                ephemeral=True
            )
            return

        # Sort by tier (descending), then by RR (descending)
        leaderboard_data.sort(key=lambda x: (x["tier"], x["rr"]), reverse=True)

        # Create embed
        embed = discord.Embed(
            title="🏆 Server Leaderboard",
            description=f"Ranked leaderboard of {len(leaderboard_data)} linked accounts",
            color=0xFFD700  # Gold color
        )

        # Add top 3 with medals
        medals = ["🥇", "🥈", "🥉"]

        for idx, player in enumerate(leaderboard_data[:15], 1):  # Limit to top 15
            medal = medals[idx - 1] if idx <= 3 else f"**{idx}.**"

            # Get rank color for visual appeal
            rank_color = get_rank_color(player["tier"])

            embed.add_field(
                name=f"{medal} {player['discord_name']}",
                value=f"**{player['rank']}** ({player['rr']} RR)\n`{player['valorant_name']}`",
                inline=False
            )

        if len(leaderboard_data) > 15:
            embed.set_footer(text=f"Showing top 15 of {len(leaderboard_data)} players")
        else:
            embed.set_footer(text=f"Total: {len(leaderboard_data)} players")

        embed.timestamp = discord.utils.utcnow()

        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(f"❌ Error creating leaderboard: {str(e)}")

@bot.tree.command(name="rank", description="Shows current rank and RR of the player")
@app_commands.describe(
    name="Riot ID Name (optional if account is linked)",
    tag="Riot ID Tag (optional if account is linked)",
    region="Region (eu, na, ap, kr)"
)
async def rank(interaction: discord.Interaction, name: str = None, tag: str = None, region: str = None):
    await interaction.response.defer()

    try:
        # Check for linked account if name/tag not provided
        if not name or not tag:
            linked = get_linked_account(interaction.user.id)
            if linked:
                name = name or linked.get("name")
                tag = tag or linked.get("tag")
                region = region or linked.get("region", DEFAULT_REGION)
            else:
                await interaction.followup.send(
                    "❌ No account linked! Use `/linkacc` to link your account or provide name and tag.",
                    ephemeral=True
                )
                return

        # Use default region if not specified
        if not region:
            region = DEFAULT_REGION
        # Get MMR data
        mmr_data = valorant_api.get_mmr(region, name, tag)

        if not mmr_data or mmr_data.get("status") != 200:
            await interaction.followup.send(f"❌ Rank-Information for **{name}#{tag}** not found.")
            return

        data = mmr_data["data"]
        current_data = data.get("current_data", {})

        # Get rank info
        current_rank = current_data.get("currenttierpatched", "Unranked")
        ranking_in_tier = current_data.get("ranking_in_tier", 0)
        mmr_change_last_game = current_data.get("mmr_change_to_last_game", 0)
        elo = current_data.get("elo", 0)

        # Calculate exact RR change over last 10 matches using MMR History API
        mmr_change_10_matches = "N/A"
        try:
            # Use v1 MMR History endpoint which has exact RR changes per match
            mmr_history_url = f"{valorant_api.base_url}/v1/mmr-history/{region}/{name}/{tag}"
            print(f"DEBUG: Fetching MMR history from: {mmr_history_url}")

            import requests
            response = requests.get(mmr_history_url, headers=valorant_api.headers)

            if response.status_code == 200:
                mmr_history_data = response.json()

                if mmr_history_data.get("status") == 200:
                    history = mmr_history_data.get("data", [])
                    print(f"DEBUG: Found {len(history)} matches in MMR history")

                    # Sum exact RR changes from last 10 matches
                    total_rr = 0
                    matches_counted = 0

                    for match in history[:10]:  # Take first 10 (most recent)
                        rr_change = match.get("mmr_change_to_last_game", 0)
                        total_rr += rr_change
                        matches_counted += 1

                    if matches_counted > 0:
                        mmr_change_10_matches = total_rr
                        print(f"DEBUG: Exact RR change from last {matches_counted} matches: {total_rr:+d}")
                    else:
                        print(f"DEBUG: No matches found in MMR history")
                else:
                    print(f"DEBUG: MMR history API returned status: {mmr_history_data.get('status')}")
            else:
                print(f"DEBUG: MMR history API error: {response.status_code}")
        except Exception as e:
            print(f"DEBUG: Error fetching MMR history: {e}")

        print(f"DEBUG: RR Changes - Last Match: {mmr_change_last_game:+d}, Last 10 (exact): {mmr_change_10_matches}")

        # ===== EMBED 1: Current Rank =====
        current_tier = current_data.get("currenttier", 0)
        current_embed = discord.Embed(
            title=f" {name}#{tag} - Rank",
            color=get_rank_color(current_tier)
        )

        # Set rank icon as thumbnail (top right)
        rank_icon_url = current_data.get("images", {}).get("large")
        if rank_icon_url:
            current_embed.set_thumbnail(url=rank_icon_url)

        current_embed.add_field(
            name="🏅 Current Rank",
            value=f"**{current_rank}**",
            inline=True
        )

        current_embed.add_field(
            name="⭐ RR",
            value=f"**{ranking_in_tier}** RR",
            inline=True
        )

        current_embed.add_field(name="\u200b", value="\u200b", inline=True)

        current_embed.add_field(
            name="📊 RR Change (1 Match)",
            value=f"**{mmr_change_last_game:+d}**",
            inline=True
        )

        # Format the 10-match change
        if isinstance(mmr_change_10_matches, str):
            mmr_10_display = mmr_change_10_matches
        else:
            mmr_10_display = f"{mmr_change_10_matches:+d}"

        current_embed.add_field(
            name="📈 RR Change (10 Matches)",
            value=f"**{mmr_10_display}**",
            inline=True
        )

        current_embed.set_footer(text=f"Region: {region.upper()}")
        current_embed.timestamp = discord.utils.utcnow()

        # ===== EMBED 2: Peak Rank =====
        peak_embed = None
        if "by_season" in data:
            by_season = data.get("by_season", {})

            # Find the season with the highest rank
            highest_rank_tier = 0
            peak_season_name = None
            peak_season_data = None

            for season_id, season_data in by_season.items():
                final_rank = season_data.get("final_rank", 0)
                if final_rank > highest_rank_tier:
                    highest_rank_tier = final_rank
                    peak_season_name = season_id
                    peak_season_data = season_data

            if peak_season_data and peak_season_name:
                # Convert season name (e.g., e10a6 to V25A6)
                if peak_season_name.startswith("e10a"):
                    act_number = peak_season_name[4:]
                    peak_season_display = f"V25A{act_number}"
                else:
                    peak_season_display = peak_season_name.upper()

                peak_rank_name = peak_season_data.get("final_rank_patched", "Unknown")
                peak_wins = peak_season_data.get("wins", 0)
                peak_games = peak_season_data.get("number_of_games", 0)
                peak_winrate = round((peak_wins / max(peak_games, 1)) * 100, 1)

                peak_embed = discord.Embed(
                    title=f"{name}#{tag} - Peak Rank",
                    color=get_rank_color(highest_rank_tier)
                )

                # Set peak rank icon as thumbnail
                # Construct the rank icon URL from the tier ID
                # Format: https://media.valorant-api.com/competitivetiers/{episode-id}/{tier-id}/largeicon.png
                # Episode ID for current competitive tiers: 03621f52-342b-cf4e-4f86-9350a49c6d04
                peak_rank_icon_url = f"https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/{highest_rank_tier}/largeicon.png"
                peak_embed.set_thumbnail(url=peak_rank_icon_url)

                peak_embed.add_field(
                    name="🏆 Peak Rang",
                    value=f"**{peak_rank_name}**",
                    inline=True
                )

                peak_embed.add_field(
                    name=f"📅 Season",
                    value=f"**{peak_season_display}**",
                    inline=True
                )

                peak_embed.add_field(name="\u200b", value="\u200b", inline=True)

                peak_embed.add_field(
                    name="🎮 Matches",
                    value=f"**{peak_games}**",
                    inline=True
                )

                peak_embed.add_field(
                    name="🏆 Winrate",
                    value=f"**{peak_winrate}%**",
                    inline=True
                )

                peak_embed.add_field(name="\u200b", value="\u200b", inline=True)

                peak_embed.add_field(
                    name="✅ Wins",
                    value=f"**{peak_wins}**",
                    inline=True
                )

                peak_embed.add_field(
                    name="❌ Losses",
                    value=f"**{peak_games - peak_wins}**",
                    inline=True
                )

                peak_embed.add_field(name="\u200b", value="\u200b", inline=True)

                peak_embed.set_footer(text=f"Highest rank achieved in {peak_season_display}")
                peak_embed.timestamp = discord.utils.utcnow()

        # Send both embeds
        if peak_embed:
            await interaction.followup.send(embeds=[current_embed, peak_embed])
        else:
            await interaction.followup.send(embed=current_embed)

    except Exception as e:
        await interaction.followup.send(f"❌ Error retrieving rank: {str(e)}")


if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ DISCORD_TOKEN not found in .env file!")
    else:
        bot.run(token)

