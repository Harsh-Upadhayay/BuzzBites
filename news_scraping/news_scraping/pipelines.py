# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
from datetime import date

from .items import HindustanTimesItem, CricbuzzNewsItem


class HindustanNewsScrapingPipeline:
    def __init__(self):
        pass

    def open_spider(self, spider):
        filedate = date.today().strftime("%Y%m%d")
        filename = filedate +  '_hindustan_times_news.csv'
        self.filename = open(filename, mode='w', encoding='utf_8_sig', newline='')
        self.csv_analysis = csv.writer(self.filename, quoting=csv.QUOTE_ALL)
        self.csv_analysis.writerow(
            [
                "news_id", 
                "news_time", 
                "news_url", 
                "news_title", 
                "news_description"
            ]
        )

    def close_spider(self, spider):
        self.filename.close()

    def process_item(self, item, spider):
        if isinstance(item, HindustanTimesItem):
            self.csv_analysis.writerow(
                [
                    item['news_id'], 
                    item['news_time'],
                    item['news_url'],
                    item['news_title'],
                    item['news_description']
                ]
            )



class CricbuzzNewsScrapingPipeline:
    def __init__(self):
        pass

    def open_spider(self, spider):
        filedate = date.today().strftime("%Y%m%d")
        filename = filedate +  '_cricbuzz_news.csv'
        self.filename = open(filename, mode='w', encoding='utf_8_sig', newline='')
        self.csv_analysis = csv.writer(self.filename, quoting=csv.QUOTE_ALL)
        self.csv_analysis.writerow(
            [
                "news_id", 
                "news_category", 
                "news_published_time", 
                "news_modified_time", 
                "news_url", 
                "news_title", 
                "news_description"
            ]
        )

    def close_spider(self, spider):
        self.filename.close()

    def process_item(self, item, spider):
        if isinstance(item, CricbuzzNewsItem):
            self.csv_analysis.writerow(
                [
                    item['news_id'],
                    item['news_category'], 
                    item['news_published_time'],
                    item['news_modified_time'],
                    item['news_url'], 
                    item['news_title'], 
                    item['news_description']
                ]
            )

