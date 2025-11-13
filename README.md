# Valorant Discord Bot

Ein Discord Bot für Valorant Statistiken mit der Henrik Dev API.

## Commands

### Account Management
- `/linkacc` - Link your Valorant account to use commands without entering name/tag every time
- `/unlinkacc` - Remove the linked Valorant account from your Discord profile

### Player Stats
- `/stats` - Shows player overview stats from the last 10 ranked matches (K/D, ADR, HS%, Winrate)
- `/matches` - Displays the last 10 ranked matches with detailed stats, agent, map, and RR changes
- `/rank` - Shows current rank, RR, and peak rank with MMR change tracking

### Server Features
- `/leaderboard` - Server-wide ranked leaderboard of all linked accounts sorted by highest rank

## Installation

1. Clone das Repository:
```bash
git clone https://github.com/serhat27s/valorant-discord-bot.git
cd Valorant-Discord_bot
```

2. Installiere die benötigten Pakete:
```bash
pip install -r requirements.txt
```

3. Erstelle eine `.env` Datei mit folgenden Werten:
```
DISCORD_TOKEN=dein_discord_bot_token
VALORANT_API_KEY=dein_henrikdev_api_key
```

**Hinweis:** Commands werden global synchronisiert und sind auf allen Servern verfügbar.
Nach dem Bot-Start dauert es bis zu 1 Stunde, bis Commands sichtbar werden.

4. Starte den Bot:
```bash
python bot.py
```

## Commands

### /stats
Zeigt eine Übersicht der Spielerstatistiken basierend auf den letzten 20 Competitive Matches.

**Parameter:**
- `name`: Riot ID Name (z.B. "Player")
- `tag`: Riot ID Tag (z.B. "EUW")
- `region`: Region (optional, default: eu)

**Ausgabe:**
- Durchschnittlicher Schaden pro Runde
- KDA
- Headshot %
- Winrate
- Gesamte Kills/Deaths/Assists

### /matches
Zeigt die letzten 5 Competitive Matches mit detaillierten Stats.

**Parameter:**
- `name`: Riot ID Name
- `tag`: Riot ID Tag
- `region`: Region (optional, default: eu)

**Ausgabe für jedes Match:**
- Map Name
- Agent
- Score
- K/D/A und KDA Ratio
- Headshot %
- Win/Loss Status

### /rank
Zeigt den aktuellen Rang und Ranked Rating des Spielers.

**Parameter:**
- `name`: Riot ID Name
- `tag`: Riot ID Tag
- `region`: Region (optional, default: eu)

**Ausgabe:**
- Aktueller Rang
- Ranked Rating (RR)
- MMR Change (letztes Spiel)
- ELO
- Peak Rank

## Regions

Verfügbare Regionen:
- `eu` - Europa
- `na` - Nordamerika
- `ap` - Asien-Pazifik
- `kr` - Korea

## API

Dieser Bot verwendet die [Henrik Dev Valorant API](https://docs.henrikdev.xyz/).

## Lizenz

MIT


