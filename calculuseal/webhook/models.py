from django.db import models

class Media(models.Model):
    """store images, audio, video
    currently implemented for images only
    """
    MEDIA_TYPES = (
        ('i', 'image'),
        # ('a', 'audio'),
        # ('v', 'video'),
    )
    media_type = models.CharField(max_length=1, choices=MEDIA_TYPES)
    timestamp = models.BigIntegerField(primary_key=True, default=0)
    image = models.BinaryField(blank=True, max_length=1048576)
    image_preview = models.BinaryField(blank=True, max_length=1048576)
