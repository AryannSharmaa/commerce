# Generated by Django 4.2.4 on 2023-08-22 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_bid_alter_listing_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.FloatField(),
        ),
    ]