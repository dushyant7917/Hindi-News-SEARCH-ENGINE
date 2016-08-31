# HINDI NEWS SEARCH ENGINE

##DESCRIPTION
This project is a demonstration of a full text query based search engine.
The results for the query searched by the user are shown only from hindi news domian.

##MODULES OF SEARCH ENGINE
* Web Crawling : Collect data(news) from web.
* Indexing : Form a index so that when a user enters a query, the search engine will not have to scan through all database to give the results. Instead it will use the index formed before hand to quickly show the results. 
* Ranking : While showing the results, the retrieved documents are given a score and they are displayed in a descending order of their score. The most relevant results are shown first.

##FRAMEWORKS,SOFTWARES AND RESOURCES USED 
* Python2.7 : Scripting
* Scrapy1.1 : Web Crawling
* Mongodb3.2 : Database Management
* Robomongo0.9 : Interface Application to view mongodb data
* Elasticsearch2.3 : Indexing and Ranking

##HOW TO USE IT?
**NOTE : Google the steps to install and run the softwares/frameworks mentioned in this documentation.** 
1. Install the above softwares, frameworks in you PC(any directory). 
2. Run the web crawling spider(*HNC_crawler.py*) to collect the data and store it in mongodb.
3. Index the data of mongodb using elastic search(run *index.py*).
4. Execute the *query.py* file to use the search engine and view the results.

##COPYRIGHT AND LICENSING INFORMATION
This project is an open source project. Its code can be used, distributed and modified in any form without issue of any legal license from the author.

##AUTHOR INFORMATION
* Developer : **DUSHYANT SINGH**
* Contact : **dushyant7917@gmail.com**
