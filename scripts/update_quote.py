from bs4 import BeautifulSoup
import requests
import os
import random

headers = {
    "Accept": "application/json",
    "Notion-Version": "2022-02-22",
    "Authorization": f"Bearer {os.environ['NOTION_ACCESS_TOKEN']}"
}

url = f"https://api.notion.com/v1/databases/{os.environ['QUOTES_DATABASE_ID']}/query"

response = requests.post(url, headers=headers).json()
quotes = response["results"]
quotes_id = []

for quote in quotes:
    quotes_id.append(quote["id"])

random_quote_id = random.choice(quotes_id)

# Get page content

url = f"https://api.notion.com/v1/blocks/{random_quote_id}/children"
response = requests.get(url, headers=headers).json()
blocks = response["results"]
content = ""

for block in blocks:
    if block["type"] == "paragraph":

        for text in block["paragraph"]["rich_text"]:
            content += text["plain_text"]

soup = BeautifulSoup(open("README.md"))
result = soup.find(id='quote')

result.string.replace_with(content)

with open("README.md", "wb") as f_output:
    f_output.write(soup.prettify("utf-8"))  