from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, timedelta, timezone
from config import SERVICE_ACCOUNT_FILE, SCOPES, CALENDAR_ID, TODAY

def get_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return build("calendar", "v3", credentials=creds)

def normalize_start(event):
    start = event.get("start", {}).get("dateTime")
    if not start:
        return None
    return datetime.fromisoformat(start.replace("Z", "+00:00")).astimezone(timezone.utc)

def events_equal(existing, new):
    return (
        existing.get("summary") == new.get("summary") and
        normalize_start(existing) == normalize_start(new) and
        existing.get("description") == new.get("description")
    )


def delete_events(service, dels):
    for e in dels:
        event_id = e.get("id")
        if not event_id:
            continue
        try:
            service.events().delete(
                calendarId=CALENDAR_ID,
                eventId=event_id
            ).execute()
        except Exception:
            pass



def get_existing_calendar_events(service):
    events = []
    page_token = None

    while True:
        response = service.events().list(
            calendarId=CALENDAR_ID,
            pageToken=page_token
        ).execute()

        events.extend(response.get("items", []))

        page_token = response.get("nextPageToken")
        if not page_token:
            break

    print(f"🗑 Deleting {len(events)} existing events")

    delete_events(service, events)

    # Return empty dict so everything gets recreated
    return {}
