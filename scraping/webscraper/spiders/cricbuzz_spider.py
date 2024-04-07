import scrapy
from bb_utils.news_utils import UrlParser
from ..items import NewsArticle
from datetime import datetime
from loguru import logger

class CricbuzzSpider(scrapy.Spider):
    
    name = 'cricbuzz_news'
    allowed_domains = ['www.cricbuzz.com']

    custom_settings = {
        'ITEM_PIPELINES': {
            'webscraper.pipelines.DjangoItemSavingPipeline': 1
        }
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
        category = self._filter_text(category)

        if category and ('IPL 2024') in category:

            date_published = response.css('time[itemprop="datePublished"]::attr(datetime)').get()

            news_url = response.css('meta[itemprop="mainEntityOfPage"]::attr(content)').get()
            news_title = self._filter_text(response.css('h1[itemprop="headline"]::text').get())

            description_sections = response.css('section[itemprop="articleBody"] p.cb-nws-para')
            description = ""
            for section in description_sections:
                description += section.css('::text').get() + "\n"

            description = self._filter_text(description)

            yield NewsArticle (
                news_id = str(response.meta['news_id']),
                url = news_url,
                title = news_title,
                description = description,
                published_at = self.format_date(date_published),
                category = 'IPL 2024',
                source = 'CB'
            )

    def format_date(self, time_str):
        try:
            if not time_str:
                return None
            elif "UTC" in time_str:
                components = time_str.split()
                month = components[0]
                day = components[1]
                year = components[3]
                hour, minute, second = map(int, components[5].split(':'))
                updated_time = datetime(int(year), datetime.strptime(month, '%b').month, int(day), hour, minute, second)
          
                return updated_time.astimezone()
        except ValueError as e:
            logger.error(f"Error: Input time string is not in the expected format, format is {time_str}")
            return None

    def _filter_text(self, text):
        if isinstance(text, list):
            if len(text) > 0:
                try:
                    return self._filter_text((' ').join(text))
                except:
                    return None
            return None
        else:
            if text == None:
                return None
            else:
                text = text.replace(u'\\n', u' ')
                text = text.replace(u'<br>', u' ')
                text = ' '.join(text.split())
			# return ''.join(text).strip()
        return text
