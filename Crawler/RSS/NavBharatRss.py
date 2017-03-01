try:
    import feedparser
    import requests
    import time
    from lxml import html

    from pymongo import MongoClient
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Navbharat_Times']
    collection = db['NT_RSS']

    # Getting RSS links
    page  = requests.get('http://navbharattimes.indiatimes.com/rss.cms')
    tree = html.fromstring(page.content)
    urlList = tree.xpath('//span[@class="rssp"]/a/@href')
    j = 1
    seed_list = []
    for i in urlList:
        if j <=15 :
            seed_list.append(i)
            j = j + 1

    # List to store news urls
    news_links = []

    # Getting news links
    for link in seed_list:
        feed = feedparser.parse(link)
        entries = feed['entries']

        for value in entries:
            news_links.append(value.link)
            print "Link added for scanning: " + value.link

        time.sleep(5)

    print("Scraping Started...")
    # Scraping Data
    for link in news_links:
        page = requests.get(link)
        tree = html.fromstring(page.content)
        news_url = link
        news_title = tree.xpath('//meta[@property="og:title"]/@content')
        news_keywords = tree.xpath('//meta[@name="keywords"]/@content')
        news_summary = tree.xpath('//meta[@name="description"]/@content')
        news_date_time = tree.xpath('//meta[@itemprop="datePublished"]/@content')
        news_image = tree.xpath('//meta[@name="twitter:image"]/@content')

        # Inserting data in database
        result = collection.find_one({'url': news_url})
        if result == None:
            collection.insert_one({'url': news_url, 'title': news_title, 'summary': news_summary, 'date_time': news_date_time, 'image': news_image, 'keywords': news_keywords})
        else:
            print("URL -> " + link + " has already been scraped!\nMoving to next link in the queue...")

        time.sleep(5)

    ############################################################################
    # Scraping Completed... Now data will be indexed in ES
    from elasticsearch import Elasticsearch
    l = db.News.find()

    total = db.News.count()
    count = 0
    prv = -1

    while count<total:
        try:
            # Instantiate the new Elasticsearch connection
            es = Elasticsearch("Elastic search URI")
            #es = Elasticsearch()
            count = 0
            for item in xrange(0,total):
                if count > prv:
                    prv = count
                    dt = l[item]['date_time'][0].split(",")[1]
                    dt = dt.split("+")[0]
                    es.index('hn', 'doc', {'url': [l[item]['url']],
                                                  'title': l[item]['title'],
                                                  'summary': l[item]['summary'],
                                                  'description': l[item]['summary'],
                                                  'keywords': l[item]['keywords'],
                                                  'date': dt,
                                                  'image_url': l[item]['image']
                                                 })
                    count = count + 1
                    print count, item+1
                else:
                    count = count + 1


        except Exception as e:
            print(str(e))

    print "RSS indexing completed"
    # Indexing also completed..
    ######################################################################################################


except Exception as e:
    from time import strftime,gmtime
    with open('Error_Log.txt', 'a') as the_file:
        showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        the_file.write(showtime + " | " + str(e) +'\n')
