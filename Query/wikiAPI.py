# -*- coding: UTF-8 -*-

import wikipedia

def wiki(query):
    wikipedia.set_lang("hi")
    result_list = wikipedia.search(query)
    #print(ny.title)
    #print(ny.url)
    #print(ny.summary)
    #for i in ny.images:
    #    print(i)
    #print(ny.content)
    '''
    if ny != None:
        return ny.title, ny.url, ny.images, ny.summary[0:500]
    else:
        return "No Result Found!", "#", [], ""
    '''
    titles = []
    urls = []
    summaries = []
    images = []
    for i in result_list:
        ny = wikipedia.page(i)
        titles.append(ny.title)
        urls.append(ny.url)
        summaries.append(ny.summary)
        images.append(ny.images[0])

    return titles, urls, summaries, images

query = str(raw_input("Enter query:"))
rt, ru, rs, ri = wiki(query)
for q,w,e,r in zip(rt, ru, rs, ri):
    print"***********"
    print q
    print w
    print e
    print r
