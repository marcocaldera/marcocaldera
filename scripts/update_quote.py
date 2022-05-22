from bs4 import BeautifulSoup
import requests
import os
import random
from utils import update_readme

headers = {
    "Accept": "application/json",
    "Notion-Version": "2022-02-22",
    "Authorization": f"Bearer {os.environ['NOTION_ACCESS_TOKEN']}"
}

# Get quote database data

quote_database_url = f"https://api.notion.com/v1/databases/{os.environ['QUOTES_DATABASE_ID']}/query"

response = requests.post(quote_database_url, headers=headers).json()
quotes = response["results"]
quotes_id = []

for quote in quotes:
    quotes_id.append(quote["id"])

random_quote_id = random.choice(quotes_id)

# Get quote content

url = f"https://api.notion.com/v1/blocks/{random_quote_id}/children"
response = requests.get(url, headers=headers).json()
blocks = response["results"]
content = ""

for block in blocks:
    if block["type"] == "paragraph":
        for text in block["paragraph"]["rich_text"]:
            content += text["plain_text"]

# Update README
update_readme(id='quote', elements=content)