from datetime import datetime, timedelta, timezone
from nhl_api import get_schedule
from config import LOOKAHEAD_DAYS, TODAY

# -----------------------------
# SERIES DATA
# -----------------------------
def extract_series_data(game):

    s = game.get("seriesStatus")

    if not isinstance(s, dict):
        return None, 0, 0, 0
    
    home_wins, away_wins = series_wins(s)

    return (
        s.get("seriesTitle"),
        home_wins,
        away_wins,
        s.get("gameNumberOfSeries", 0)
    )

def series_wins(s):
    top_seed_wins = s.get("topSeedWins", 0)
    bottom_seed_wins = s.get("bottomSeedWins", 0)
    game_number=s["gameNumberOfSeries"]
    is_top_home = game_number in {1,2,5,7}
    home_seed_wins = top_seed_wins if is_top_home else bottom_seed_wins
    away_seed_wins = bottom_seed_wins if is_top_home else top_seed_wins

    return home_seed_wins, away_seed_wins

def get_games_from_nhl():
    games = []

    gameDict = {}

    for i in range(-1, LOOKAHEAD_DAYS):

        date = (TODAY + timedelta(days=i)).isoformat()
        data = get_schedule(date)

        print(i, data)

        for day in data.get("gameWeek", []):
            for g in day.get("games", []):
                if g["gameState"] == "OFF" or g["gameScheduleState"] == "TBD":
                    continue

                start = datetime.fromisoformat(g["startTimeUTC"].replace("Z", "+00:00"))

                gameDict[str(g.get("id"))] = g

    for g in gameDict.values():
        title, home_wins, away_wins, game_number = extract_series_data(g)

        games.append({
            "game_id": str(g.get("id")),
            "home": g["homeTeam"]["abbrev"],
            "away": g["awayTeam"]["abbrev"],
            "start": g["startTimeUTC"],
            "series_title": title,
            "home_wins": home_wins,
            "away_wins": away_wins,
            "game_number_of_series": game_number,
        })
    
    print(f"Games fetched from NHL: {len(games)}")
    # print_games_summary(games)

    return games


def print_games_summary(games):

    print("\n📅 GAMES SUMMARY:")

    for g in games:
        dt_object = datetime.fromisoformat(g['start'])
        readable_time = dt_object.strftime("%B %d, %I:%M %p")

        print(
            f"🧩 {g['away']} ({g['away_wins']}) @ {g['home']} ({g['home_wins']}) | {readable_time} | {g['game_id']}"
        )