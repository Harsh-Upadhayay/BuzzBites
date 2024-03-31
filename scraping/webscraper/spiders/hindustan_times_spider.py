import scrapy
from bb_utils.news_utils import TextHandler
from ..items import HindustanTimesNews

class HindustanTimesSpider(scrapy.Spider):
    
    name = 'hindustan_times'
    allowed_domains = ['www.hindustantimes.com']

    custom_settings = {
        'ITEM_PIPELINES': {'webscraper.pipelines.HindustanNewsScrapingPipeline': 300}
    }

    def start_requests(self):
        url = "https://www.hindustantimes.com/topic/ipl/news"

        yield scrapy.Request(
            url=url,
            callback=self.parse_news,
        )

    def parse_news(self, response):
        newsList = response.css('div.cartHolder')

        for news in newsList:

            yield scrapy.Request(
                url = news.attrib['data-weburl'],
                callback = self.parse_data,
                meta={
                    'item': {
                        'news_id' : news.attrib['data-vars-storyid'],
                        'news_url' : news.attrib['data-weburl'],
                        'news_title' : TextHandler()._filter_text(news.attrib['data-vars-story-title']),
                        'news_time' : news.attrib['data-vars-story-time']
                    } 
                }
            )

    def parse_data(self, response):
        news_item = response.meta['item']
        story_content = []

        news_details = response.css('div.storyDetails p')
        for news_p in news_details:
            story_content.append(news_p.css("::text").get())

        yield HindustanTimesNews (
            news_id = news_item['news_id'],
            news_url = news_item['news_url'],
            news_title = news_item['news_title'],
            news_description = TextHandler()._filter_text(story_content),
            created_at = news_item['news_time'],
        )
