import scrapy
from ..utils import TextHandler
from ..items import HindustanTimesItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError

class HindustanTimesSpider(scrapy.Spider):
    
    name = 'hindustan_times'
    allowed_domains = ['www.hindustantimes.com']
    error_page = open('hindustan_times_error_page.log','a')

    custom_settings = {
        'ITEM_PIPELINES': {'news_scraping.pipelines.HindustanNewsScrapingPipeline': 300}
    }

    def start_requests(self):
        url = "https://www.hindustantimes.com/topic/ipl/news"

        yield scrapy.Request(
            url=url,
            callback=self.parse_news,
            errback=self.errback_httpbin,
        )

    def parse_news(self, response):
        newsList = response.css('div.cartHolder')

        for news in newsList:
            news_item = HindustanTimesItem()

            news_item['news_id'] = news.attrib['data-vars-storyid']
            news_item['news_url'] = news.attrib['data-weburl']
            news_item['news_title'] = TextHandler()._filter_text(news.attrib['data-vars-story-title'])
            news_item['news_time'] = news.attrib['data-vars-story-time']

            yield scrapy.Request(
                url = news.attrib['data-weburl'],
                callback = self.parse_data,
                meta={'item': news_item}
            )

    def parse_data(self, response):
        news_item = response.meta['item']
        story_content = []

        news_details = response.css('div.storyDetails p')
        for news_p in news_details:
            story_content.append(news_p.css("::text").get())

        news_item['news_description'] = TextHandler()._filter_text(story_content)
        
        yield news_item


    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
            self.error_page.write(response.url+'\n')
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
            self.error_page.write(request.url+'\n')
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.error_page.write(request.url+'\n')