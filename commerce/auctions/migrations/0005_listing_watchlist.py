# Generated by Django 4.0.2 on 2022-05-10 11:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_comment_user_alter_listing_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
