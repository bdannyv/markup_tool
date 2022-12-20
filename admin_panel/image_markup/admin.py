from django.contrib import admin

from .models import ImageClass, ImageTable, Label


class LabelInline(admin.TabularInline):
    model = Label
    extra = 1
    verbose_name = 'Image labels'


@admin.register(ImageClass)
class ImageClassAdmin(admin.ModelAdmin):
    list_display = 'name',


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_filter = 'user', 'image', 'type'
    search_fields = 'user', 'image'


@admin.register(ImageTable)
class ImageTableAdmin(admin.ModelAdmin):
    inlines = LabelInline,
    list_filter = 'image',
