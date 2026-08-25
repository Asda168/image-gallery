from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Photo


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "photo_count")
    prepopulated_fields = {"slug": ("name",)}

    def photo_count(self, obj):
        return obj.photos.count()


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("thumb", "title", "category", "photographer", "is_featured", "likes", "uploaded_at")
    list_filter = ("category", "is_featured", "uploaded_at")
    search_fields = ("title", "description", "photographer")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_featured",)

    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:48px;width:48px;object-fit:cover;border-radius:6px;" />',
                obj.image.url,
            )
        return ""

    thumb.short_description = "Preview"
