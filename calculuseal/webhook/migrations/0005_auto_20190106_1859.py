# Generated by Django 2.1.4 on 2019-01-06 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0004_auto_20190106_1855'),
    ]

    operations = [
        migrations.RenameField(
            model_name='media',
            old_name='media_type',
            new_name='content_type',
        ),
    ]
