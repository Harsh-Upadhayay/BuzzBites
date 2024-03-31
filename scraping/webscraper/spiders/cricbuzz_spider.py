import scrapy
from bb_utils.news_utils import TextHandler, UrlParser
from ..items import CricbuzzNews

class CricbuzzSpider(scrapy.Spider):
    
    name = 'cricbuzz_news'
    allowed_domains = ['www.cricbuzz.com']

    custom_settings = {
        'ITEM_PIPELINES': {'webscraper.pipelines.CricbuzzNewsScrapingPipeline': 300}
    }

    def start_requests(self):
        url = "https://www.cricbuzz.com/cricket-news"

        yield scrapy.Request(
            url=url,
            callback=self.parse_news
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

            date_published = response.css('time[itemprop="datePublished"]::attr(datetime)').get()
            date_modified = response.css('time[itemprop="dateModified"]::attr(datetime)').get()

            news_url = response.css('meta[itemprop="mainEntityOfPage"]::attr(content)').get()
            news_title = response.css('h1[itemprop="headline"]::text').get()

            description_sections = response.css('section[itemprop="articleBody"] p.cb-nws-para')
            description = ""
            for section in description_sections:
                description += section.css('::text').get() + "\n"


            yield CricbuzzNews (
                news_id = TextHandler()._filter_text(response.meta['news_id']),
                news_url = news_url,
                news_title = TextHandler()._filter_text(news_title),
                news_description = TextHandler()._filter_text(description),
                created_at = TextHandler()._filter_text(date_published),
                news_category = category
            )
