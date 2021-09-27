from ics import Calendar, Event
from pathlib import Path
from datetime import datetime
import pandas as pd
from dateutil.tz import tzlocal, tzutc


def get_events(file_path):
    return pd.read_csv(file_path).to_dict('records')


def create_calendar(events):
    calendar = Calendar()
    for event in events:
        e = Event()
        e.name = event['name']
        f, t = to_date(event)
        e.begin = f
        e.end = t
        calendar.events.add(e)
    return calendar


def to_date(event):
    input_format = '%d.%m.%Y %H:%M'
    output_format = '%Y-%m-%d %H:%M:%S %Z'
    f = datetime.strptime(f'{event["date"]} {event["from"]}', input_format).replace(tzinfo=tzlocal())
    t = datetime.strptime(f'{event["date"]} {event["to"]}', input_format).replace(tzinfo=tzlocal())
    return f.astimezone(tzutc()).strftime(output_format), t.astimezone(tzutc()).strftime(output_format)


def save_calendar(calendar, file_path):
    with open(file_path, 'w') as file:
        file.write(str(calendar))


if __name__ == '__main__':
    BASE_DIR = Path(__file__).parent
    EVENTS_FILE = BASE_DIR / 'events.csv'
    CALENDAR_FILE = BASE_DIR / 'import.ics'

    events = get_events(EVENTS_FILE)
    calendar = create_calendar(events)
    save_calendar(calendar, CALENDAR_FILE)
