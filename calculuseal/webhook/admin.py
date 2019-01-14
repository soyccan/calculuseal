from django.contrib import admin

from webhook import models

# admin.site.register(models.Media)
# admin.site.register(models.Friends)

@admin.register(models.Media)
class MediaAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Friends)
class FriendsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'display_name', 'status_message', 'picture_url')
