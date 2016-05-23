__author__ = 'shushi'
# -*- coding: utf-8 -*-

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule
from wangyinews.items import Tech163Item

class Spider(CrawlSpider):
    name = "news"
    allowed_domains = ["sports.163.com"]
    start_urls = ['http://sports.163.com/']
    rules = (
        Rule(
            LinkExtractor(allow = r"/16/05\d+/\d+/*"),
            #代码中的正则/15/06\d+/\d+/*的含义是大概是爬去/15/06开头并且后面是数字/数字/任何格式/的新闻
            callback = "parse_news",
            follow = True
            #follow=ture定义了是否再爬到的结果上继续往后爬
            ),
        )

    def parse_news(self, response):
        item = Tech163Item()

        self.get_title(response,item)
        self.get_source(response,item)
        self.get_url(response,item)
        self.get_text(response,item)

        return item

    def  get_title(self,response,item):
        title = response.xpath("/html/head/title/text()").extract()
        if title:
            item['title'] = title[0][:-5]

    def get_source(self,response,item):
        source = response.xpath("//div[@class='post_time_source']/text()").extract()
        if source:
            item['time'] = source[0][17:-17]

    def get_text(self,response,item):
        news_body = response.xpath("//div[@id='endText']/p/text()").extract()

        if news_body:
            str = ''.join(news_body)
            item['body'] = str

    def get_url(self,response,item):
        news_url = response.url
        if news_url:
            item['url'] = news_url







