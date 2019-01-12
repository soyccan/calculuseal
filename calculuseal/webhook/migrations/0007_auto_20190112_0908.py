# Generated by Django 2.1.4 on 2019-01-12 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0006_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friends',
            name='display_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='friends',
            name='picture_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='friends',
            name='status_message',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
