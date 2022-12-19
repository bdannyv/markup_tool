from django.db import models
from image_markup.models.base import TimeStampMixin, UUIDMixin

# Create your models here.


class ImageClasses(models.IntegerChoices):
    UNKNOWN = 0
    DOG = 1
    CAT = 2


class ImageTable(UUIDMixin, TimeStampMixin, models.Model):
    class Meta:
        db_table = "image_storage"

    image = models.ImageField(null=False, blank=False, upload_to='images/')


class Label(UUIDMixin, TimeStampMixin, models.Model):
    class Meta:
        db_table = 'image_label'

    type = models.IntegerField(choices=ImageClasses.choices, default=ImageClasses.UNKNOWN)
    image = models.ForeignKey('ImageTable', on_delete=models.CASCADE)
    user_id = models.UUIDField(null=False, blank=False)  # Detail stored in auth service
