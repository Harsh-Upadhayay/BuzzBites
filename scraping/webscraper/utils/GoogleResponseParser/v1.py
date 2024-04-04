from .base import GoogleSearchResponseParserBase
import re
from loguru import logger

class GoogleSearchResponseParserV1(GoogleSearchResponseParserBase):
    
    def image_sources(self, response):
        
        urls = []
        img_ids = response.css('div[jsaction="TMn9y:cJhY7b;;cFWHmd:s370ud;"] ::attr(data-tbnid)').getall()
        
        pattern = r'\{\s*"444383007"\s*:.+?\}'

        matches = re.findall(pattern, response.text)
        
        for match in matches:
            pattern = r'http[^ ^"]+'
        
            try:
                urls.append(re.findall(pattern, match)[1])
            except IndexError:
                # If the image url is not found, skip the item.
                pass
            except Exception as e:
                logger.error(f"Error in parse: {e}")
        
        return urls
