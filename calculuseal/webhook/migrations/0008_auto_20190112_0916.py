# Generated by Django 2.1.4 on 2019-01-12 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0007_auto_20190112_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friends',
            name='display_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='friends',
            name='picture_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='friends',
            name='status_message',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='data',
            field=models.BinaryField(max_length=1048576),
        ),
        migrations.AlterField(
            model_name='media',
            name='preview_data',
            field=models.BinaryField(max_length=1048576),
        ),
    ]
