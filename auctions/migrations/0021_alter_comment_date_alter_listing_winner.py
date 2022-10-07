# Generated by Django 4.1 on 2022-10-07 13:32

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_listing_winner_creator_alter_comment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 7, 13, 32, 13, 814502)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='winner',
            field=models.ForeignKey(default=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to=settings.AUTH_USER_MODEL),
        ),
    ]
