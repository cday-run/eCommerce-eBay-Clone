# Generated by Django 3.0.8 on 2020-07-20 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.CharField(default='no image', max_length=255),
        ),
    ]