from django.contrib import admin

from .models import TagDescription, Submission


class TagDescriptionAdmin(admin.ModelAdmin):
    list_display = ( 'tag_name', 'title', 'description', )

admin.site.register(TagDescription, TagDescriptionAdmin)


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'creator', 'featured', 'hidden', 'tags', 'modified', )

admin.site.register(Submission, SubmissionAdmin)

