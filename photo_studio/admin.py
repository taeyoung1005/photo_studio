from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import User, Album, Photo, Photo_templates

# Register your models here.
admin.site.register(User)
admin.site.register(Album)
admin.site.register(Photo)


class Photo_templatesAdmin(admin.ModelAdmin):
    list_display = ['id', 'property', 'template_image']

    def template_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.template.url,
            width=200,
            height=200,
        )
        )
    template_image.short_description = 'Thumbnail'


admin.site.register(Photo_templates, Photo_templatesAdmin)
