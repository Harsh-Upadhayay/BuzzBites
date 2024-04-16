from django.db import models
from django.db.models import UniqueConstraint
from asgiref.sync import sync_to_async
from django.utils import timezone
from django.db.utils import IntegrityError


class Meme(models.Model):
    STATUS_CHOICES = [
        ('downloaded', 'File was downloaded'),
        ('uptodate', 'File was not downloaded, as it was downloaded recently, according to the file expiration policy'),
        ('cached', 'File was already scheduled for download, by another item sharing the same file'),
    ]

    search_tag = models.CharField(
        max_length=100,
        help_text="Input tag with which the spider will scrape memes.",
    )
    img_url = models.CharField(
        max_length=400, help_text="Source URL of the meme. (ends with .jpg, .png, etc.)"
    )
    local_path = models.CharField(
        max_length=200,
        null=True,
        default=None,
        help_text="Path where the meme is stored on the server.",
    )
    checksum = models.CharField(
        max_length=32,
        null=True,
        default=None,
        help_text="Checksum of the meme image.",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        help_text="Scraping status of the meme image.",
    )   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    @sync_to_async
    def async_save(self):
        try:
            self.save()
        except IntegrityError:
            existing_obj = Meme.objects.get(checksum=self.checksum)
            existing_obj.updated_at=timezone.now()
            existing_obj.save()
        except:
            pass    
        
    class Meta:
        ordering = ['-updated_at']
        constraints = [UniqueConstraint(fields=['checksum'], name='unique_checksum')]
        

class NewsArticle(models.Model):
    SOURCE_CHOICES = [
        ('CB', 'Cricbuzz news'),
        ('HT', 'Hindustan Times news')
    ]

    news_id = models.CharField(
        max_length=32,
        null=True,
        default=None,
    )
    title = models.TextField(blank=True)
    description = models.TextField(blank=True)
    summary = models.TextField(blank=True, null=True)
    summary_hindi = models.TextField(blank=True, null=True)
    source = models.CharField(
        max_length=255,
        choices=SOURCE_CHOICES
    )
    url = models.URLField(max_length=400)
    category = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    published_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        constraints = [UniqueConstraint(fields=['news_id'], name='unique_newsid')]

    @sync_to_async
    def async_save(self):
        try:
            self.save()
        except IntegrityError:
            try:
                existing_obj = NewsArticle.objects.get(news_id=self.news_id)
                existing_obj.check_or_update_fields(self)
            except NewsArticle.DoesNotExist:
                pass

    def check_or_update_fields(self, new_instance):
        """
        Update the fields of the current NewsArticle instance with the fields from new_instance.
        Only update fields that have changed.
        """

        field_updated = False
        exclude_fields = ['id', 'created_at', 'updated_at', 'summary', 'summary_hindi']

        for field in self._meta.fields:
            field_name = field.name
            if field_name in exclude_fields:
                continue

            current_value = getattr(self, field_name)
            new_value = getattr(new_instance, field_name)

            if current_value != new_value:
                setattr(self, field_name, new_value)
                field_updated = True
    
        if field_updated:
            self.updated_at = timezone.now()
            self.save()


class MatchReport(models.Model):
    SOURCE_CHOICES = [
        ('IPLT20', 'IPL official website'),
    ]

    report_id = models.CharField(
        max_length=32,
        null=True,
        default=None,
    )
    title = models.TextField(blank=True)
    description = models.TextField(blank=True)
    summary = models.TextField(blank=True, null=True)
    summary_hindi = models.TextField(blank=True, null=True)
    source = models.CharField(
        max_length=255,
        choices=SOURCE_CHOICES
    )
    url = models.URLField(max_length=400)
    category = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    match_no = models.IntegerField(
        null=True
    )
    published_at = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        constraints = [UniqueConstraint(fields=['report_id'], name='unique_reportid')]

    @sync_to_async
    def async_save(self):
        try:
            self.save()
        except IntegrityError:
            try:
                existing_obj = NewsArticle.objects.get(report_id=self.report_id)
                existing_obj.check_or_update_fields(self)
            except NewsArticle.DoesNotExist:
                pass

    def check_or_update_fields(self, new_instance):
        """
        Update the fields of the current NewsArticle instance with the fields from new_instance.
        Only update fields that have changed.
        """

        field_updated = False
        exclude_fields = ['id', 'created_at', 'updated_at', 'summary', 'summary_hindi']

        for field in self._meta.fields:
            field_name = field.name
            if field_name in exclude_fields:
                continue

            current_value = getattr(self, field_name)
            new_value = getattr(new_instance, field_name)

            if current_value != new_value:
                setattr(self, field_name, new_value)
                field_updated = True
    
        if field_updated:
            self.updated_at = timezone.now()
            self.save()