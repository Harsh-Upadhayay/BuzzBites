import scrapy
from ..spider_inputs import google_search_queries, team_names, player_names
from ..items import Meme
import re
from loguru import logger

class GoogleSearchSpider(scrapy.Spider):
    name = 'google_search'
    
    def __init__(self, query, time_frame='', *args, **kwargs):
        super(GoogleSearchSpider, self).__init__(*args, **kwargs)
        self.base_url = 'https://www.google.com/search?q={query}&tbm=isch{time_frame}'
        self.time_frame = time_frame
        self.query = query
        
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
        else:
            return ''
            
    def parse(self, response):
        
        img_ids = response.css('div[jsaction="TMn9y:cJhY7b;;cFWHmd:s370ud;"] ::attr(data-tbnid)').getall()
        pattern = r'\{\s*"444383007"\s*:.+?\}'

        matches = re.findall(pattern, response.text)
        
        for match in matches:
            pattern = r'http[^ ^"]+'
            
            try:
                url = (re.findall(pattern, match)[1])
                yield Meme(search_tag=self.query, img_url=url)    
                
            except IndexError:
                # If the image url is not found, skip the item.
                pass
            except Exception as e:
                logger.error(f"Error in parse: {e}")
                

