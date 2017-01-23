#!/usr/bin/env python3

try:
    import requests
    from bs4 import BeautifulSoup

    import time
    from time import gmtime, strftime

    def RSSlinks():
        agent = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}

        RSS_URLS = []
        req = requests.get("http://www.amarujala.com/rss", headers=agent)
        soup = BeautifulSoup(req.content, "html.parser")
        for i in soup.find_all('td', attrs={"style": "width: 400px;"}):
            if i.text[0] == 'h':
                RSS_URLS.append(i.text)

        return RSS_URLS

    # Using Mongodb as database
    from pymongo import MongoClient
    client = MongoClient('mongodb://localhost:27017/')
    db = client['RSS-database']
    collection = db['RSS-news']

    # Getting all the RSS links
    RSS_urls = RSSlinks()

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
        req = requests.get(link, headers=agent)
        soup = BeautifulSoup(req.content, "html.parser")

        # Finding news title
        title = soup.find('meta', attrs={'name': 'twitter:title'})
        if title != None:
            news_title = title.get('content').replace("- Amarujala", "")
        else:
            time.sleep(5)
            continue

        # Finding news image
        img = soup.find('meta', attrs={'name': 'twitter:image'})
        if img != None:
            news_image = img.get('content')
        else:
            time.sleep(5)
            continue

        # Finding news image
        kw = soup.find('meta', attrs={'name': 'keywords'})
        if kw != None:
            news_keywords = kw.get('content').split(",")
        else:
            time.sleep(5)
            continue

        # Finding news summary
        summary = soup.find('meta', attrs={'property': 'og:description'})
        if summary != None:
            news_summary = summary.get('content')
        else:
            time.sleep(5)
            continue

        # Finding news date
        dt = soup.find('span', attrs={'datetime': True})
        if dt != None:
            news_date_time = dt.text.split(", ")[-1]
        else:
            time.sleep(5)
            continue

        # Inserting data in database
        result = collection.find_one({'url': link})
        if result == None:
            collection.insert_one({'url': link, 'title': news_title, 'summary': news_summary, 'date_time': news_date_time, 'image': news_image, 'keywords': news_keywords})
        else:
            print("URL -> " + link + " has already been scraped!\nMoving to next link in the queue...")

        time.sleep(5)



except Exception as e:
    with open('Error_Log.txt', 'a') as the_file:
        showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        the_file.write(showtime + " | " + str(e) +'\n')
