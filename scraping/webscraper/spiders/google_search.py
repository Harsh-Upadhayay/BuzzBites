import scrapy
from ..items import Meme
import re
from loguru import logger
from ..utils.googleImageSearchParser import ParserBuilder

class GoogleSearchSpider(scrapy.Spider):
    name = 'google_search'
    
    def __init__(self, query, time_frame='', *args, **kwargs):
        super(GoogleSearchSpider, self).__init__(*args, **kwargs)
        self.base_url = 'https://www.google.com/search?q={query}&tbm=isch{time_frame}'
        self.time_frame = time_frame
        self.query = query
        self.parser = ParserBuilder.build('2')
        
    def start_requests(self):
        url = self.base_url.format(query=self.query, time_frame=self.get_time_frame())
        yield scrapy.Request(url, callback=self.parse)
    
    def get_time_frame(self):
        if self.time_frame == 'day':
            return '&tbs=qdr:d'
        elif self.time_frame == 'month':
            return '&tbs=qdr:m'
        elif self.time_frame == 'year':
            return '&tbs=qdr:y'
        elif self.time_frame == 'week':
            return '&tbs=qdr:w'
        elif self.time_frame == 'hour':
            return '&tbs=qdr:h'
        else:
            return ''
            
    def parse(self, response):
                
        urls = self.parser.image_sources(response)

        for url in urls:
            try:
                yield Meme(search_tag=self.query, img_url=url)    
            except Exception as e:
                logger.exception(e)
                
                

