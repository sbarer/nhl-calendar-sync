from datetime import timezone, datetime

CALENDAR_ID = "16fdfaaccc9c5b7d801bc543490fbed0dc897012649b883b53a1dad93188c7a2@group.calendar.google.com"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

SERVICE_ACCOUNT_FILE = "key.json"

LOOKAHEAD_DAYS = 7
GAME_DURATION_HOURS = 3

TODAY = datetime.now(timezone.utc).date()