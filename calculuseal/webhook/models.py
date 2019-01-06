from django.db import models

class Media(models.Model):
    """store images, audio, video
    content_type: mimetype
    timestamp: integer, Unix epoch time * 1000, for precision to milliseconds
    data: binary data
    preview_data: binary data for preview
    """
    content_type = models.CharField(max_length=100)
    timestamp = models.BigIntegerField(primary_key=True, default=0)
    data = models.BinaryField(blank=True, max_length=1048576) # 1M
    preview_data = models.BinaryField(blank=True, max_length=1048576)
