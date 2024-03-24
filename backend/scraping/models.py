from django.db import models

# Create your models here.


class meme(models.Model):
    search_tag = models.CharField(
        max_length=100,
        help_text="Input tag with which the spider will scrape memes.",
    )
    remote_url = models.CharField(
        max_length=100, help_text="Source URL of the meme. (ends with .jpg, .png, etc.)"
    )
    local_path = models.CharField(
        max_length=200,
        null=True,
        default=None,
        help_text="Path where the meme is stored on the server.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
