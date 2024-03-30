from django.db import models
from django.db.models import UniqueConstraint
from asgiref.sync import sync_to_async
from django.utils import timezone
from django.db.utils import IntegrityError
# Create your models here.


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
        