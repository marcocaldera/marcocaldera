import json
from bs4 import BeautifulSoup
import requests
import os
import random
from datetime import datetime
import calendar
from utils import update_readme

headers = {
    "Accept": "application/json",
    "Notion-Version": "2022-02-22",
    "Authorization": f"Bearer {os.environ['NOTION_ACCESS_TOKEN']}"
}

# Get quote database data

habit_database_url = f"https://api.notion.com/v1/databases/{os.environ['HABIT_DATABASE_ID']}/query"

response = requests.post(habit_database_url, headers=headers).json()
habits_calendar = response["results"]
current_date = datetime.now()

habit_counters = {"read": 0}

for habit in habits_calendar:
    day = habit["properties"]["Date"]["formula"]["date"]["start"]
    date_time = datetime.strptime(day, '%Y-%m-%dT%H:%M:%S.000+00:00')

    if date_time.month == current_date.month and habit["properties"]["Read"]["checkbox"]:
        habit_counters["read"] += 1

with open("data/habits.json", "w") as f:
    f.write(json.dumps(habit_counters))

print(habit_counters["read"] / current_date.day * 100)