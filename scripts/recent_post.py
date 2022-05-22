from bs4 import BeautifulSoup
import requests
from utils import update_readme


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

url = "https://marcocaldera.com/post-sitemap.xml"
post_sitemap = requests.get(url, headers=headers).text

soup = BeautifulSoup(post_sitemap, "xml")
posts = soup.find_all('url')

html_post_links = ""

for post in posts[:3]:
    link = post.find('loc').string

    post_source = requests.get(link, headers=headers).text
    post_soup = BeautifulSoup(post_source)

    title = post_soup.find(class_='entry-title').string
    published_time = post_soup.find("meta", property='article:published_time')["content"]
    
    html_post_links += f"<a href={link}>{title}</a><br/>"

posts_list_soup = BeautifulSoup('<p align="center" id="recent-post">' + html_post_links + "</p>", "html.parser")

# Update README
update_readme(id="recent-post", elements=posts_list_soup) 