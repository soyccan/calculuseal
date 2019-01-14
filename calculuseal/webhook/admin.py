from django.contrib import admin

from webhook import models

@admin.register(models.Media)
class MediaAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Friends)
class FriendsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'display_name', 'status_message', 'picture_url')

@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user_id', 'text')
    date_hierarchy = 'timestamp'
