from datetime import datetime, timedelta
from config import GAME_DURATION_HOURS

def build_event(g):
    
    series_title=g["series_title"]
    start = datetime.fromisoformat((g["start"]).replace("Z", "+00:00"))
    end = start + timedelta(hours=GAME_DURATION_HOURS)

    return {
        "summary": f"{g['away']} ({g['away_wins']}) @ {g['home']} ({g['home_wins']})",
        "description": (
            f"Playoff Round: {series_title}\n"
            f"Game: {g['game_number_of_series']}\n"
        ),
        "start": {
            "dateTime": start.isoformat(),
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": end.isoformat(),
            "timeZone": "UTC"
        },
        "extendedProperties": {
            "private": {
                "game_id": str(g["game_id"])
            }
        }
    }