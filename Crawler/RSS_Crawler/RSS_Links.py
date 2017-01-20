# Python 3 script

import requests
from bs4 import BeautifulSoup

def RSSlinks():
    agent = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}

    RSS_URLS = []
    req = requests.get("http://www.amarujala.com/rss", headers=agent)
    soup = BeautifulSoup(req.content, "html.parser")
    for i in soup.find_all('td', attrs={"style": "width: 400px;"}):
        if i.text[0] == 'h':
            RSS_URLS.append(i.text)

    return RSS_URLS
