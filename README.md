# HINDI NEWS SEARCH ENGINE

## DESCRIPTION
This project is a demonstration of a full text query based search engine.
The results for the query searched by the user are shown only from hindi news domian.

## MODULES OF SEARCH ENGINE
* Web Crawling : Collect data(news) from web.
* Indexing : Form a index so that when a user enters a query, the search engine will not have to scan through all database to give the results. Instead it will use the index formed before hand to quickly show the results. 
* Ranking : While showing the results, the retrieved documents are given a score and they are displayed in a descending order of their score. The most relevant results are shown first.

## FRAMEWORKS,SOFTWARES AND RESOURCES USED 
* Python2.7 : Scripting
* Scrapy1.1 : Web Crawling
* Mongodb3.2 : Database Management
* Robomongo0.9 : Interface Application to view mongodb data
* Elasticsearch2.3 : Indexing and Ranking
* Flask0.11.1 : Inteface between elastic search and website(http://localhost:5000)
* Google Transliterate API : Real time conversion of english text(query entered by user) into hindi query

## HOW TO USE IT?
**NOTE : Google the steps to install and run the softwares/frameworks mentioned in this documentation.** 
* Install the above softwares, frameworks in you PC(any directory). 
* Run the web crawling spider(*HNC_crawler.py*) to collect the data and store it in mongodb.
* Index the data of mongodb using elastic search(run *index.py*).
* Run the *app.py* file from **Query directory** to use your PC as the server and use the search engine on *http://localhost:5000* on your web browser.

## COPYRIGHT AND LICENSING INFORMATION
This project is an open source project. Its code can be used, distributed and modified in any form without issue of any legal license from the author.

## AUTHOR INFORMATION
* Developer : **DUSHYANT SINGH**
* Contact : **dushyant7917@gmail.com**

## OTHER CONTRIBUTORS
* Rudrangshu Nandi : **github.com/Rud156**
* Tilak Patidar : **github.com/tilakpatidar**
