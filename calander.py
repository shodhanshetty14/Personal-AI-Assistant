from datetime import datetime, timezone
import os.path
import warnings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

logging.basicConfig(filename='./logs/error.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

warnings.filterwarnings("ignore")
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def ReadEvents():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    # print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
    #   print("No upcoming events found.")
      return "No upcomming Events"

    # Prints the start and name of the next 10 events
    print(f"AI: Upcoming Events: ")
    for event in events:
        start = event["start"].get("dateTime")
        # start = event["start"].get("dateTime", event["start"].get("date"))
        print("\t", start, event["summary"])
    return events

  except HttpError as error:
    logging.error("An error occurred: %s", error)
    # print(f"An error occurred: {error}")
    return "Error Occured try again"



def CreateEvents(start_time, end_time, event_summary, event_description="", attendees=[]):
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    try:
        service = build("calendar", "v3", credentials=creds)
    
        event = {
        "start": {
        "dateTime": start_time,
        "timeZone": "UTC"  # Explicitly specify the time zone
        },
        "end": {
        "dateTime": end_time,
        "timeZone": "UTC"
        },
        "summary": event_summary,
        "description": event_description,
        "attendees": attendees
    }

        event = service.events().insert(calendarId="primary", body=event).execute()
        
        # print("Event created:", event.get("htmlLink"))
        return event

    except Exception as e:
        # print(e)
        logging.error("An error occurred: %s", e)
        return "Error Occured try again"
   
     



if __name__ == "__main__":
    ReadEvents()
    CreateEvents()
    
    # start_time = datetime(2023, 12, 21, tzinfo=timezone.utc).isoformat()
    # end_time = datetime(2023, 12, 21, tzinfo=timezone.utc).isoformat()
    # event_summary = "Holiday Party"
    # description = "It is Holiday Party"
    # # attendees = []
    # created_event = create_event(start_time, end_time, event_summary, event_description=description)
    
    # print("Event summary:", created_event['summary'])
    # print("Start time:", created_event['start']['dateTime'])
    # print("End time:", created_event['end']['dateTime'])
    # print("Description:", created_event.get('description'))  # Optional field
    # print("Attendees:", created_event.get('attendees'))  # Optional field
    # print("Event link:", created_event.get('htmlLink')) 