import requests
from typing import Optional, Dict, Any

class ValorantAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.henrikdev.xyz/valorant"
        self.headers = {
            "Authorization": api_key
        }

    def get_account(self, name: str, tag: str) -> Optional[Dict[str, Any]]:
        """Get account information"""
        url = f"{self.base_url}/v1/account/{name}/{tag}"
        print(f"DEBUG: Getting account from: {url}")
        response = requests.get(url, headers=self.headers)

        print(f"DEBUG: Account API response status: {response.status_code}")

        if response.status_code == 200:
            return response.json()
        else:
            try:
                error_data = response.json()
                print(f"DEBUG: Account API error: {error_data}")
            except:
                print(f"DEBUG: Account API error (no JSON): {response.text}")

        return None

    def get_mmr(self, region: str, name: str, tag: str) -> Optional[Dict[str, Any]]:
        """Get rank and MMR information"""
        url = f"{self.base_url}/v2/mmr/{region}/{name}/{tag}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        return None

    def get_match_history(self, region: str, name: str, tag: str, mode: str = "competitive", size: int = 5) -> Optional[Dict[str, Any]]:
        """Get recent match history"""
        url = f"{self.base_url}/v3/matches/{region}/{name}/{tag}?mode={mode}&size={size}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        return None


    def get_all_act_matches(self, region: str, name: str, tag: str, mode: str = "competitive") -> Optional[Dict[str, Any]]:
        """Get last 10 matches from current act"""
        print(f"DEBUG: Fetching last 10 matches from current act")

        # Get matches from v3 API
        matches = self.get_match_history(region, name, tag, mode=mode, size=10)

        if not matches or matches.get("status") != 200:
            print(f"DEBUG: v3 API failed")
            return None

        # Filter by current act
        filtered = self.filter_matches_by_act(matches)
        filtered_count = len(filtered.get('data', []))
        print(f"DEBUG: v3 API returned {filtered_count} matches in current act")

        return filtered


    def filter_matches_by_act(self, matches_data: Dict[str, Any]) -> Dict[str, Any]:
        """Filter matches to only include current act"""
        if not matches_data or "data" not in matches_data:
            return matches_data

        # Get the most recent match's season info
        if not matches_data["data"]:
            return matches_data

        current_season = matches_data["data"][0].get("metadata", {}).get("season", {}).get("short", "")

        # Filter matches that belong to the current season
        filtered_matches = []
        for match in matches_data["data"]:
            match_season = match.get("metadata", {}).get("season", {}).get("short", "")
            if match_season == current_season:
                filtered_matches.append(match)

        # Create new data structure with filtered matches
        filtered_data = matches_data.copy()
        filtered_data["data"] = filtered_matches

        return filtered_data

    def get_current_season_name(self, region: str, name: str, tag: str) -> str:
        """Get current season name from MMR API and convert to readable format"""
        try:
            mmr_data = self.get_mmr(region, name, tag)
            if mmr_data and mmr_data.get("status") == 200:
                by_season = mmr_data.get("data", {}).get("by_season", {})
                if by_season:
                    # The last key is the most recent season
                    season_keys = list(by_season.keys())
                    if season_keys:
                        current_season = season_keys[-1]
                        print(f"DEBUG: Current season from MMR API: {current_season}")

                        # Convert e10aX to V25AX (Episode 10 was renamed to V25)
                        if current_season.startswith("e10a"):
                            act_number = current_season[4:]  # Get the act number after "e10a"
                            converted = f"V25A{act_number}"
                            print(f"DEBUG: Converted {current_season} to {converted}")
                            return converted

                        return current_season
        except Exception as e:
            print(f"DEBUG: Error getting season name: {e}")

        return "Unknown Act"


    def calculate_stats(self, matches_data: Dict[str, Any], name: str, tag: str) -> Dict[str, float]:
        """Calculate overall stats from match history"""
        if not matches_data or "data" not in matches_data:
            return {}

        total_kills = 0
        total_deaths = 0
        total_assists = 0
        total_headshots = 0
        total_bodyshots = 0
        total_legshots = 0
        total_damage = 0
        total_damage_received = 0
        total_rounds = 0
        wins = 0
        total_matches = 0

        print(f"DEBUG: Calculating stats for {len(matches_data['data'])} matches")

        for match in matches_data["data"]:
            players = match.get("players", {}).get("all_players", [])

            # Find player in match
            for player in players:
                player_name = player.get("name", "").lower()
                player_tag = player.get("tag", "").lower()

                if player_name == name.lower() and player_tag == tag.lower():
                    stats = player.get("stats", {})

                    total_kills += stats.get("kills", 0)
                    total_deaths += stats.get("deaths", 0)
                    total_assists += stats.get("assists", 0)

                    # Damage dealt handling - try multiple possible structures
                    damage_data = stats.get("damage", {})
                    match_damage = 0

                    if isinstance(damage_data, dict):
                        # Try "made" field
                        match_damage = damage_data.get("made", 0)
                        # If made is 0, try "damage" field
                        if match_damage == 0:
                            match_damage = damage_data.get("damage", 0)
                    elif isinstance(damage_data, (int, float)):
                        match_damage = damage_data

                    # If still 0, try alternative locations
                    if match_damage == 0:
                        match_damage = stats.get("damage_made", 0)
                        if match_damage == 0:
                            # Try getting from damage_delta or other fields
                            damage_delta_val = player.get("damage_made", 0)
                            if damage_delta_val > 0:
                                match_damage = damage_delta_val

                    total_damage += match_damage

                    # Damage received handling
                    match_damage_received = player.get("damage_received", 0)
                    if match_damage_received == 0:
                        # Try alternative location
                        damage_recv_data = stats.get("damage", {})
                        if isinstance(damage_recv_data, dict):
                            match_damage_received = damage_recv_data.get("received", 0)

                    total_damage_received += match_damage_received

                    # Count rounds played in this match
                    rounds_played = match.get("metadata", {}).get("rounds_played", 0)
                    total_rounds += rounds_played

                    # Debug first match to see structure
                    if total_matches == 0 and match_damage == 0:
                        print(f"DEBUG: First match damage structure:")
                        print(f"  stats.damage: {stats.get('damage')}")
                        print(f"  stats keys: {list(stats.keys())}")
                        print(f"  player keys: {list(player.keys())}")

                    # Headshot stats
                    total_headshots += stats.get("headshots", 0)
                    total_bodyshots += stats.get("bodyshots", 0)
                    total_legshots += stats.get("legshots", 0)

                    # Check if won
                    player_team = player.get("team", "").lower()
                    if player_team == "red" and match.get("teams", {}).get("red", {}).get("has_won", False):
                        wins += 1
                    elif player_team == "blue" and match.get("teams", {}).get("blue", {}).get("has_won", False):
                        wins += 1

                    total_matches += 1
                    break

        # Calculate averages
        kda = ((total_kills + total_assists) / max(total_deaths, 1))
        # ADR = Average Damage per Round (not per match!)
        adr = total_damage / max(total_rounds, 1)
        avg_damage_received_per_round = total_damage_received / max(total_rounds, 1)
        damage_delta = adr - avg_damage_received_per_round
        total_shots = total_headshots + total_bodyshots + total_legshots
        hs_percentage = (total_headshots / max(total_shots, 1)) * 100
        winrate = (wins / max(total_matches, 1)) * 100

        print(f"DEBUG: Stats calculated - Total Damage: {total_damage}, Received: {total_damage_received}, Matches: {total_matches}, Rounds: {total_rounds}, ADR: {adr}, DDΔ: {damage_delta}")

        return {
            "kda": round(kda, 2),
            "avg_damage": round(adr, 1),  # ADR per round
            "damage_delta": round(damage_delta, 1),  # DDΔ per round
            "hs_percentage": round(hs_percentage, 1),
            "winrate": round(winrate, 1),
            "kills": total_kills,
            "deaths": total_deaths,
            "assists": total_assists,
            "matches": total_matches
        }

