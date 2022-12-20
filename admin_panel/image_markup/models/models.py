from django.contrib.auth.models import User
from django.db import models
from image_markup.models.base import TimeStampMixin, UUIDMixin

# Create your models here.


class ImageClass(TimeStampMixin, models.Model):
    class Meta:
        db_table = 'image_class'
        verbose_name_plural = 'Classes'

    name = models.CharField("name", max_length=255)

    def __str__(self):
        return f'{self.name}'


class ImageTable(UUIDMixin, TimeStampMixin, models.Model):
    class Meta:
        db_table = "image_storage"
        verbose_name_plural = 'Images'

    image = models.ImageField('image', null=False, blank=False, upload_to='images/')
    image_class = models.ManyToManyField("ImageClass", through="Label")

    def __str__(self):
        return f"Image {self.id}"


# TODO: poor naming
class Label(UUIDMixin, TimeStampMixin, models.Model):
    class Meta:
        db_table = 'image_label'
        verbose_name_plural = 'Labels'
        constraints = [
            models.UniqueConstraint(fields=['image'], name='unique image')
        ]

    type = models.ForeignKey('ImageClass', on_delete=models.CASCADE)
    image = models.ForeignKey('ImageTable', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type} {self.id}'
