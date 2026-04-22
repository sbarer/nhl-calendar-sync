from datetime import timezone, datetime
from events import build_event
from calendar_client import get_service, get_existing_calendar_events, CALENDAR_ID, events_equal
from games import get_games_from_nhl
from config import TODAY

service = get_service()

def main():
    print("🚀 NHL SYNC START")

    # -----------------------------
    # Fetch schedule
    # -----------------------------
    games = get_games_from_nhl()

    # -----------------------------
    # EXISTING EVENTS
    # -----------------------------
    existing_calendar_events = get_existing_calendar_events(service)

    created = 0
    updated = 0
    skipped = 0

    sample_update_event = None
    sample_created_event = None

    # -----------------------------
    # Sync loop
    # -----------------------------
    for game in games:
        event = build_event(game)

        existing_event = existing_calendar_events.get(str(game["game_id"]))

        start_time = datetime.fromisoformat(
            game["start"].replace("Z", "+00:00")
        ).astimezone(timezone.utc)

        now = datetime.now(timezone.utc)
        # -----------------------------
        # UPDATE
        # -----------------------------
        if existing_event:
            if events_equal(existing_event, event) or start_time < now:
                skipped += 1
                continue

            service.events().update(
                calendarId=CALENDAR_ID,
                eventId=existing_event["id"],
                body=event
            ).execute()

            updated += 1

            if not sample_update_event:
                sample_update_event = event
            
        # -----------------------------
        # CREATE
        # -----------------------------
        else:
            try:
                service.events().insert(
                    calendarId=CALENDAR_ID,
                    body=event,
                    sendUpdates="none"
                ).execute()

                created += 1

                if not sample_created_event:
                    sample_created_event = event

            except Exception as e:
                if "already exists" in str(e):
                    pass  # safe ignore duplicate
                else:
                    raise

    # -----------------------------
    # Debug output
    # -----------------------------
    if sample_update_event:
        print("\n🧪 SAMPLE UPDATE EVENT:")
        print(sample_update_event)

    if sample_created_event:
        print("\n🧪 SAMPLE CREATED EVENT:")
        print(sample_created_event)

    print("\n=================================================")
    print(f"Created: {created}")
    print(f"Skipped: {skipped}")
    print(f"Updated: {updated}")
    print("✅ SYNC COMPLETE")


if __name__ == "__main__":
    main()