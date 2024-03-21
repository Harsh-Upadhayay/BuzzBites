BOT_NAME = "news_scraping"

SPIDER_MODULES = ["news_scraping.spiders"]
NEWSPIDER_MODULE = "news_scraping.spiders"

# LOG_LEVEL = 'WARNING'
LOG_FILE = 'error.log'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "news_scraping.middlewares.NewsScrapingDownloaderMiddleware": 543,
#}

# Configure item pipelines
# ITEM_PIPELINES = {
#    "news_scraping.pipelines.HindustanNewsScrapingPipeline": 500,
# }

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
