import json
import requests
import os
from datetime import datetime

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Notion-Version": "2022-02-22",
    "Authorization": f"Bearer {os.environ['NOTION_ACCESS_TOKEN']}"
}

# Habits
HABIT_I = "Read"
HABIT_II = "Mental Health"
HABIT_III = "Fitness"

# Get habits from the database data

habit_database_url = f"https://api.notion.com/v1/databases/{os.environ['HABIT_DATABASE_ID']}/query"
habits_calendar = []
request_params = {}
has_more = True

while has_more:
    response = requests.post(habit_database_url, headers=headers, data=json.dumps(request_params)).json()
    habits_calendar += response["results"]
    has_more = response["has_more"]
    request_params["start_cursor"] = response["next_cursor"]

current_date = datetime.now()

habit_counters = {"read": 0, "mental_health": 0, "fitness": 0}

for habit in habits_calendar:
    day = habit["properties"]["Date"]["formula"]["date"]["start"]
    date_time = datetime.strptime(day, '%Y-%m-%dT%H:%M:%S.000+00:00')

    # HABIT_I
    if date_time.month == current_date.month and habit["properties"][HABIT_I]["checkbox"]:
        habit_counters["read"] += 1

    # HABIT_II
    if date_time.month == current_date.month and habit["properties"][HABIT_II]["checkbox"]:
        habit_counters["mental_health"] += 1

    # HABIT_III
    if date_time.month == current_date.month and habit["properties"][HABIT_III]["checkbox"]:
        habit_counters["fitness"] += 1

with open("data/habits.json", "w") as f:
    f.write(json.dumps(habit_counters))