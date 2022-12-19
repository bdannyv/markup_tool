from django.contrib import admin

from .models import ImageTable, Label


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_filter = 'user_id', 'image', 'type'
    search_fields = 'user_id', 'image'


@admin.register(ImageTable)
class ImageTableAdmin(admin.ModelAdmin):
    list_filter = 'image',
