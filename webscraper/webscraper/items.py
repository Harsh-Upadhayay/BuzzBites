# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
import scrapy
from scraping import models


class Meme(DjangoItem):
    # define the fields for your item here like:
    django_model = models.Meme
    image_urls = scrapy.Field()
    images = scrapy.Field()
