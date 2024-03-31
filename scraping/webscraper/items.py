# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
import scrapy
from scraping import models


class Meme(DjangoItem):
    django_model = models.Meme

class HindustanTimesNews(DjangoItem):
    django_model = models.HindustanTimesNews

class CricbuzzNews(DjangoItem):
    django_model = models.CricbuzzNews
