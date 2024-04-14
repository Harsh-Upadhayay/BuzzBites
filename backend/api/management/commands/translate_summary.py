from django.core.management.base import BaseCommand
from django.db.models import Q
from mtranslate import translate
from scraping.models import NewsArticle

class Command(BaseCommand):
    help = 'Translate the news_summary to Hindi'

    def handle(self, *args, **options):
        self.translate_summary()
        self.stdout.write(self.style.SUCCESS('Translation of summary is done successfully.'))


    def translate_summary(self):
 
        articles = NewsArticle.objects.filter(summary__isnull=False, summary_hindi__isnull=True)
        
        for article in articles:
            hindi_summary = translate(article.summary, 'hi')
            article.summary_hindi = hindi_summary
            article.save()
