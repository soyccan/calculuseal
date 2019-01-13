from django.contrib import admin

from webhook import models

admin.site.register(models.Media)
admin.site.register(models.Friends)
