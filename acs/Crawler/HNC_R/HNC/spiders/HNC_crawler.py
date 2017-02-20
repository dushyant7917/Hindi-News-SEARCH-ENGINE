# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from HNC.items import HncItem

class HncCrawlerSpider(CrawlSpider):
    name = 'HNC_crawler'
    allowed_domains = ['jagran.com']
    start_urls = ['http://www.jagran.com/search/news']

    rules = [
        Rule(LinkExtractor(allow='',restrict_xpaths=('//ul[@class="listing"]/li/h3/a')),callback='parse_item', follow=True),
        Rule(LinkExtractor(allow='',restrict_xpaths=('//a[@class="next-btn"]')), follow=True),
    ]

    def parse_item(self, response):
        item = HncItem()

        item['url'] = Selector(response).xpath('//meta[@property="og:url"]/@content').extract()
        item['title'] = Selector(response).xpath('//section[@class="title"]/h1/text()').extract()
        item['summary'] = Selector(response).xpath('//div[@class="article-summery"]/text()').extract()
        item['description'] = Selector(response).xpath('//meta[@property="og:description"]/@content').extract()
        item['keywords'] = Selector(response).xpath('//meta[@itemprop="keywords"]/@content').extract()
        item['date_time'] = Selector(response).xpath('//meta[@http-equiv="Last-Modified"]/@content').extract()
        item['image_url'] = Selector(response).xpath('//meta[@name="twitter:image"]/@content').extract()

        yield item
