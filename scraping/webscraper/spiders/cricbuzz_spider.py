import scrapy
from ..utils import TextHandler, UrlParser
from ..items import HindustanTimesItem, CricbuzzNewsItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError

class HindustanTimesSpider(scrapy.Spider):
    
    name = 'cricbuzz_news'
    allowed_domains = ['www.cricbuzz.com']
    error_page = open('cricbuzz_error_page.log','a')

    custom_settings = {
        'ITEM_PIPELINES': {'news_scraping.pipelines.CricbuzzNewsScrapingPipeline': 300}
    }

    def start_requests(self):
        url = "https://www.cricbuzz.com/cricket-news"

        yield scrapy.Request(
            url=url,
            callback=self.parse_news,
            errback=self.errback_httpbin,
        )

    def parse_news(self, response):
        latest_news_url = response.css('a.cb-nws-hdln-ancr::attr(href)').get()
        latest_news_id = UrlParser(latest_news_url).get_latest_news_id()
        
        for i in range(100):
            news_id = int(latest_news_id) - i
            news_url = f"https://www.cricbuzz.com/cricket-news/{news_id}/1"

            yield scrapy.Request(
                url = news_url,
                callback = self.parse_data,
                meta = {'news_id' : news_id}
            )

    def parse_data(self, response):

        category = response.css('div.cb-nws-sub-txt span.cb-text-gray::text').get()
        category = TextHandler()._filter_text(category)


        if ('IPL 2024') in category:
            news_item = CricbuzzNewsItem()
            news_item['news_category'] = category
            news_item['news_id'] = response.meta['news_id']

            date_published = response.css('time[itemprop="datePublished"]::attr(datetime)').get()
            news_item['news_published_time'] = TextHandler()._filter_text(date_published)

            date_modified = response.css('time[itemprop="dateModified"]::attr(datetime)').get()
            news_item['news_modified_time'] = TextHandler()._filter_text(date_modified)

            news_url = response.css('meta[itemprop="mainEntityOfPage"]::attr(content)').get()
            news_item['news_url'] = news_url

            news_title = response.css('h1[itemprop="headline"]::text').get()
            news_item['news_title'] = TextHandler()._filter_text(news_title)

            description_sections = response.css('section[itemprop="articleBody"] p.cb-nws-para')
            description = ""
            for section in description_sections:
                description += section.css('::text').get() + "\n"
            news_item['news_description'] = TextHandler()._filter_text(description)
        
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