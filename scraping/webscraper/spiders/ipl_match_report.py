import scrapy
from bb_utils.news_utils import UrlParser, TextHandler
from ..items import MatchReport
from datetime import datetime
from loguru import logger
import re

class IPLT20Spider(scrapy.Spider):
    
    name = 'match_report'
    allowed_domains = ['www.iplt20.com']

    custom_settings = {
        'ITEM_PIPELINES': {
            'webscraper.pipelines.DjangoItemSavingPipeline': 1
        }
    }

    def start_requests(self):
        url = "https://www.iplt20.com/news/match-reports"

        yield scrapy.Request(
            url=url,
            callback=self.parse_reports
        )

    def parse_reports(self, response):
        latest_report_url = response.css('a[data-type="match-reports"]::attr(href)').get()
        latest_report_id = UrlParser(latest_report_url).get_latest_news_id()

        for i in range(200):
            report_id = int(latest_report_id) - i
            report_url = f"https://www.iplt20.com/news/{report_id}/1"

            yield scrapy.Request(
                url = report_url,
                callback = self.parse_data,
                meta = {
                    'report_id' : report_id,
                    'url' : latest_report_url
                }
            )

    def parse_data(self, response):
        title = response.css('div.vn-blogBanTitle h2::text').get()
        title = TextHandler()._filter_text(title)
        if title and 'Match Report' in title:
            match_no = re.search(r'Match (\d+)', title)
            if match_no:
                match_no = int(match_no.group(1))
            else:
                match_no = None

            published_time = response.css('div.vn-blogBanTitle p span::text').get()
            published_time = TextHandler()._filter_text(published_time)

            story_content = []
            for paragraph in response.css('div.vn-blogDetCntInr > p'):
                story_content.append(paragraph.css("::text").get())
            description = TextHandler()._filter_text(story_content)

            category = 'IPL 2024'
            if ('IPL 2024') in title:
                category = 'IPL 2024'
            elif ('IPL 2023') in title:
                category = 'IPL 2023'
            elif ('IPL 2022') in title:
                category = 'IPL 2022'

            yield MatchReport(
                report_id = response.meta['report_id'],
                url = response.meta['url'],
                match_no = match_no,
                title = title,
                description = description,
                published_at = published_time,
                source = 'IPLT20',
                category = category
            )

