# Generated by Django 2.1.4 on 2019-01-14 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0009_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, primary_key=True, serialize=False),
        ),
    ]
