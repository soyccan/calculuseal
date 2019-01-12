from django.db import models
from django.core.validators import RegexValidator

class Media(models.Model):
    """store images, audio, video
    content_type: mimetype
    timestamp: integer, Unix epoch time * 1000, for precision to milliseconds
    data: binary data
    preview_data: binary data for preview
    """
    content_type = models.CharField(max_length=100)
    timestamp = models.BigIntegerField(primary_key=True, default=0)
    data = models.BinaryField(max_length=1048576) # 1M
    preview_data = models.BinaryField(max_length=1048576)

class Friends(models.Model):
    user_id = models.CharField(
        primary_key=True,
        max_length=33,
        validators=[RegexValidator(r'^U[0-9a-f]{32}$',
                                   message='Invalid LINE User ID')])
    display_name = models.CharField(null=True, blank=True, max_length=100)
    status_message = models.CharField(null=True, blank=True, max_length=500)
    picture_url = models.URLField(null=True, blank=True, max_length=200)
