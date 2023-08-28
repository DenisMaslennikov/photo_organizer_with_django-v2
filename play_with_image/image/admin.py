from django.contrib import admin
from django.utils.safestring import mark_safe

from sorl.thumbnail import get_thumbnail

from .models import Image


class ImageAdmin(admin.ModelAdmin):
    filter_horizontal = ["tags"]
    readonly_fields = ["preview"]
    list_display = ["name", "preview_small"]
    list_display_links = ["name", "preview_small"]

    @staticmethod
    def preview(obj):
        return mark_safe(
            f'<img src="' f'{get_thumbnail(obj.image.path, "450").url}">'
        )

    @staticmethod
    def preview_small(obj):
        return mark_safe(
            f'<img src="'
            f'{get_thumbnail(obj.image.path, "100x100", crop="center").url}">'
        )


admin.site.register(Image, ImageAdmin)
