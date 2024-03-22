import scrapy
import argparse
from ..spider_inputs import google_search_queries, team_names, player_names
from ..items import WebscraperItem
import re

class GoogleSearchSpider(scrapy.Spider):
    name = 'google_search'
    
    def __init__(self, time_frame='', *args, **kwargs):
        super(GoogleSearchSpider, self).__init__(*args, **kwargs)
        self.base_url = 'https://www.google.com/search?q={query}&tbm=isch{time_frame}'
        self.time_frame = time_frame
    
    def generate_queries(self):
        generated_queries = []

        for query in google_search_queries:
            if "{team_name}" in query:
                for team_name in team_names:
                    generated_query = query.replace("{team_name}", team_name)
                    generated_queries.append(generated_query)
            elif "{player_name}" in query:
                for player_name in player_names:
                    generated_query = query.replace("{player_name}", player_name)
                    generated_queries.append(generated_query)
            else:
                generated_queries.append(query)

        return generated_queries
        
    def start_requests(self):
        queries = self.generate_queries()
        queries = queries[:1]
        for query in queries:
            url = self.base_url.format(query=query, time_frame=self.get_time_frame())
            yield scrapy.Request(url, callback=self.parse, meta={'query': query})
    
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
        ct = 0
        urls = []
        for match in matches:
            
        # print(match)

            pattern = r'http[^ ^"]+'

            try:
                url = (re.findall(pattern, match)[1])
                
                yield(WebscraperItem(image_urls=[url]))
            except:
                pass

