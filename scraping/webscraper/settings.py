from decouple import config
import sys, os, django

# Path initializations for Django project

sys.path.append(config('BUZZBITE_PATH'))
from bb_utils import backend_path
sys.path.append(backend_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()


BOT_NAME = "webscraper"
SPIDER_MODULES = ["webscraper.spiders"]
NEWSPIDER_MODULE = "webscraper.spiders"
ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
   "scrapy.pipelines.images.ImagesPipeline": 1
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

IMAGES_STORE = config('IMAGES_STORE')
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
