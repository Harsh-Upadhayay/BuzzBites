
import hashlib
from itemadapter import ItemAdapter
import os
from decouple import config
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from loguru import logger

from scrapy.exceptions import DropItem

from scrapy.http.request import NO_CALLBACK
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes

class ImageProcessingPipeline(ImagesPipeline):
    settings = get_project_settings() 

    """
    Pipeline for downloading images from URLs.

    Overrides:
        file_path(self, request, response=None, info=None, *, item=None): 
            Customize the download path of each file.
        get_media_requests(item, info): 
            Return a Request for each file URL.
        item_completed(results, item, info): 
            Called when all file requests for a single item have completed.

    Example:
        class MyFilesPipeline(CustomFilesPipeline):
            def file_path(self, request, response=None, info=None, *, item=None):
                return "files/" + PurePosixPath(urlparse(request.url).path).name

    """
    def file_path(self, request, response=None, info=None, *, item=None):
        req_url_hash = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"{req_url_hash}.jpg"

    def get_media_requests(self, item, info):
        img_url = ItemAdapter(item)['img_url']
        return Request(img_url, callback=NO_CALLBACK, headers={'Accept': 'image/*'})

    def item_completed(self, results, item, info):
        try:
            for ok, data in results:
                if ok:
                    item['local_path'] = os.path.join(config('IMAGES_STORE'), data['path'])
                    item['checksum'] = data['checksum']
                    item['status'] = data['status']

        except Exception as e:
            logger.error(f"Error in item_completed: {e}")
        
        if item.get('local_path') is None:
            # Drop images whose download failed.
            raise DropItem("Image download failed")
        
        return item


class DjangoItemSavingPipeline:
    async def process_item(self, item, spider):
        
        dj_item = item.save(commit=False)
        await (dj_item.async_save())
        
        return item