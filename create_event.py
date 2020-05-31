from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import datetime

# What the program can access within Calendar
# See more at https://developers.google.com/calendar/auth
scopes = ["https://www.googleapis.com/auth/calendar"]

flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)

# Use this to pull the users credentials into a pickle file
#credentials = flow.run_console()
#pickle.dump(credentials, open("token.pkl", "wb"))

# Read the credentials from a saved pickle file
credentials = pickle.load(open("token.pkl", "rb"))

# Build the calendar resource
service = build("calendar", "v3", credentials=credentials)

# Store a list of Calendars on the account
result = service.calendarList().list().execute()
calendar_id = result["items"][1]["id"]

result = service.events().list(calendarId=calendar_id).execute()

def create_event(shift_information):
    """
    Create a Google Calendar Event

    Args:
        my_event: dictionary
    """
    print("Created Event for " + str(shift_information[2]))

    year = shift_information[2].year
    month = shift_information[2].month
    day = shift_information[2].day
    start_hour = int(shift_information[0][0:2])
    start_min = int(shift_information[0][-2:])
    end_hour = int(shift_information[1][0:2])
    end_min = int(shift_information[1][-2:])

    start_date_time = datetime.datetime(year, month, day, start_hour, start_min)
    end_date_time = datetime.datetime(year, month, day, end_hour, end_min)

    event = {
        "summary": 'Work',
        "location": 'Carlow D/T MSA',
        "description": 'Shift',
        "start": {
            "dateTime": start_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "timeZone": "Europe/London",
        },
        "end": {
            "dateTime": end_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "timeZone": "Europe/London",
        },
        "reminders": {
            "useDefault": False,
        },
    }

    return service.events().insert(calendarId=calendar_id, body=event, sendNotifications=True).execute()