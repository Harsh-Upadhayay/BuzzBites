# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HindustanTimesItem(scrapy.Item):
    
    news_id = scrapy.Field()
    news_time = scrapy.Field()
    news_url = scrapy.Field()
    news_title = scrapy.Field()
    news_description = scrapy.Field()


    def set_all(self, value):
        for keys, _ in self.fields.items():
            self[keys] = value


class CricbuzzNewsItem(scrapy.Item):
    
    news_category = scrapy.Field()
    news_id = scrapy.Field()
    news_published_time = scrapy.Field()
    news_modified_time = scrapy.Field()
    news_url = scrapy.Field()
    news_title = scrapy.Field()
    news_description = scrapy.Field()


    def set_all(self, value):
        for keys, _ in self.fields.items():
            self[keys] = value
