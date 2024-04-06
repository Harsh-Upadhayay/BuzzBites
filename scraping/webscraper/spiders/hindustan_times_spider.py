import scrapy
from ..items import NewsArticle

class HindustanTimesSpider(scrapy.Spider):
    name = 'hindustan_times'
    start_urls = ['https://www.hindustantimes.com/topic/ipl/news']

    custom_settings = {
        'ITEM_PIPELINES': {
            'webscraper.pipelines.DjangoItemSavingPipeline': 1
        }
    }

    def parse(self, response):
        for news in response.css('div.cartHolder'):
            news_id = news.attrib.get('data-vars-storyid', '')
            news_url = news.attrib.get('data-weburl', '')
            news_title = self._filter_text(news.attrib.get('data-vars-story-title', ''))
            news_time = news.attrib.get('data-vars-story-time', '')

            yield scrapy.Request(
                url=news_url,
                callback=self.parse_data,
                meta={
                    'news_id': news_id,
                    'news_url': news_url,
                    'news_title': news_title,
                    'news_time': news_time
                }
            )

    def parse_data(self, response):
        news_id = response.meta['news_id']
        news_url = response.meta['news_url']
        news_title = response.meta['news_title']
        news_time = response.meta['news_time']

        story_content = []
        for news_p in response.css('div.storyDetails p'):
            story_content.append(news_p.css("::text").get())
        
        yield NewsArticle(
            news_id=news_id,
            url=news_url,
            title=news_title,
            description=self._filter_text(story_content),
            published_at=news_time,
            category='IPL 2024',
            source='HT'
        )

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