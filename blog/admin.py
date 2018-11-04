from django.contrib import admin

from .models import Blog, Category, Images


class ImagesInline(admin.TabularInline):
    model = Images
    extra = 0


class BlogAdmin(admin.ModelAdmin):
    inlines = [
        ImagesInline,
    ]


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category)
admin.site.register(Images)
