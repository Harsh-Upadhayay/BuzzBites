from decouple import config
import sys, os, django

# Path initializations for Django project

sys.path.append(config('BUZZBITE_PATH'))
from bb_utils import backend_path, root_path
sys.path.append(backend_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()

LOG_FILE = 'scrapy.log'
LOG_LEVEL = 'ERROR'
BOT_NAME = "webscraper"
SPIDER_MODULES = ["webscraper.spiders"]
NEWSPIDER_MODULE = "webscraper.spiders"
ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
   "webscraper.pipelines.ImageProcessingPipeline": 1,
   "webscraper.pipelines.DjangoItemSavingPipeline": 2
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

IMAGES_STORE = os.path.join(root_path, config('IMAGES_STORE'))

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
