import scrapy
from bb_utils.news_utils import UrlParser
from ..items import MatchReport
from datetime import datetime
from loguru import logger

class IPLT20Spider(scrapy.Spider):
    
    name = 'match_report'
    allowed_domains = ['www.iplt20.com']

    custom_settings = {
        'ITEM_PIPELINES': {
            'webscraper.pipelines.DjangoItemSavingPipeline': 1
        }
    }