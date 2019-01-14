import datetime

from django.contrib import admin

from calculuseal import settings
from webhook import models

@admin.register(models.Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('show_timestamp', 'show_data', 'content_type')
    change_list_template = 'admin/webhook/media/change_list.html'

    def show_timestamp(self, obj):
        return datetime.datetime.fromtimestamp(obj.timestamp / 1000).__str__()

    def show_data(self, obj):
        return f'<img src="https://{settings.SERVER_NAME}/media/{obj.timestamp}/">'

@admin.register(models.Friends)
class FriendsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'display_name', 'status_message', 'picture_url')

@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user_id', 'text')
    date_hierarchy = 'timestamp'
