# Python 3 script

import requests
from bs4 import BeautifulSoup
import RSS_Links

import time

# Using Mongodb as database
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['RSS-database']
collection = db['RSS-news']

# Getting all the RSS links
RSS_urls = RSS_Links.RSSlinks()

agent = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}

# List to store URL(s) for actual scraping of news data
NEWS_URLS = []


for article_link in RSS_urls:
    req = requests.get(article_link, headers=agent)
    soup = BeautifulSoup(req.content, "xml")
    for i in soup.find_all('link'):
        if i.text != "http://www.amarujala.com" and i.text not in NEWS_URLS:
            NEWS_URLS.append(i.text)


for link in NEWS_URLS:
    try:
        req = requests.get(link, headers=agent)
        soup = BeautifulSoup(req.content, "html.parser")

        # Finding news title
        title = soup.find('meta', attrs={'name': 'twitter:title'})
        news_title = title.get('content').replace("- Amarujala", "")
        #print(news_title)

        # Finding news image
        img = soup.find('meta', attrs={'name': 'twitter:image'})
        news_image = img.get('content')
        #print(news_image)

        # Finding news image
        kw = soup.find('meta', attrs={'name': 'keywords'})
        news_keywords = kw.get('content').split(",")
        #print(news_keywords)

        # Finding news summary
        summary = soup.find('meta', attrs={'property': 'og:description'})
        news_summary = summary.get('content')
        #print(news_summary)

        # Finding news date
        dt = soup.find('span', attrs={'datetime': True})
        news_date_time = dt.text.split(", ")[-1]
        #print(news_date_time)

        # Inserting data in database
        result = collection.find_one({'url': link})
        if result == None:
            collection.insert_one({'url': link, 'title': news_title, 'summary': news_summary, 'date_time': news_date_time, 'image': news_image, 'keywords': news_keywords})
        else:
            print("URL -> " + link + " has already been scraped!\nMoving to next link in the queue...")

    except:
        with open('Error_Log.txt', 'a') as the_file:
            the_file.write('Some Error Occured\n')
