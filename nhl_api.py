import requests
from datetime import datetime

def get_schedule(date):
    return requests.get(
        f"https://api-web.nhle.com/v1/schedule/{date}"
    ).json()


def get_game(game_id):
    r = requests.get(
        f"https://api-web.nhle.com/v1/gamecenter/{game_id}/landing"
    )
    return r.json() if r.status_code == 200 else None


def get_roster(team):
    r = requests.get(
        f"https://api-web.nhle.com/v1/roster/{team}/current"
    )
    return r.json() if r.status_code == 200 else {}


def get_bracket():
    year = datetime.utcnow().year
    r = requests.get(
        f"https://api-web.nhle.com/v1/playoff-bracket/{year}"
    )
    return r.json() if r.status_code == 200 else {}
