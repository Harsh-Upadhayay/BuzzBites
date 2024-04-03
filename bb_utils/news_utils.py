import re 


class UrlParser:
    def __init__(self, url):
        self.url = url

    def get_latest_news_id(self):
        # url like : '/cricket-news/129946/better-prepared-this-time-than-we-were-two-years-ago-fleming-on-captaincy-switch'
        pattern = r"/(\d+)/"
        match = re.search(pattern, self.url)
        if match:
            return match.group(1)
        else:
            return None


class TextHandler:

    def _filter_text(self, text):
        if isinstance(text, list):
            if len(text) > 0:	
                return self._filter_text((' ').join(text))
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