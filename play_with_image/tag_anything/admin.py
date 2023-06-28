from django.contrib import admin

from .models import Tag, TagCategory

admin.site.register(Tag)
admin.site.register(TagCategory)
