# Generated by Django 5.0.4 on 2024-04-07 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0006_delete_cricbuzznews_delete_hindustantimesnews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsarticle',
            name='published_at',
            field=models.DateTimeField(null=True),
        ),
    ]