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

def date_out_of_bounds(e):
    startDate = datetime.fromisoformat(e["start"]["dateTime"].replace("Z", "+00:00")).date()
    if not startDate:
        return True
    try:
        upper = TODAY + timedelta(days=7)

        return startDate < TODAY or startDate > upper

    except Exception:
        return True


def get_existing_calendar_events(service):

    events = {}
    deletions = []

    page_token = None

    while True:

        response = service.events().list(
            calendarId=CALENDAR_ID,
            pageToken=page_token
        ).execute()

        for e in response.get("items", []):

            game_id = e.get("extendedProperties", {}).get("private", {}).get("game_id", "")

            if (
                game_id == "" or
                game_id in events or
                date_out_of_bounds(e)
            ):
                deletions.append(e)
            else:
                events[game_id] = e    

        page_token = response.get("nextPageToken")

        if not page_token:
            break

    # print(f"events = {len(events)}\ndeletions = {len(deletions)}")
    delete_events(service, deletions)
    
    # first_event = next(iter(events.values()), None)
    # print(f"existing_events ({len(events)}): {first_event}")
    # print(events.keys())
    return events
