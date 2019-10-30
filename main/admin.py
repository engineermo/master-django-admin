from django.contrib import admin

# Register your models here.
from django.utils import timezone

from .models import Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created', 'last_modified', 'is_draft', 'days_since_creation')
    list_filter = ('is_draft', 'date_created')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 50
    actions = ('set_blogs_to_published',)
    date_hierarchy = 'date_created'
    # fields = (('title', 'slug'), 'body', 'is_draft')

    fieldsets = (
        (None, {
            'fields': (('title', 'slug'), 'body'),

        }),
        ('Advanced options', {
            'fields': ('is_draft', ),
            'description': 'Options to configure blog creations'
        }),
    )

    def days_since_creation(self,Blog):
        diff = timezone.now() - Blog.date_created
        return diff.days
    days_since_creation.short_description = 'Days Active'

    def get_ordering(self, request):
        if request.user.is_superuser:
            return 'title', '-date_created'
        return 'title'

    def set_blogs_to_published(self, request, queryset):
        count = queryset.update(is_draft=False)
        self.message_user(request, ' The {} selected blogs have been published'.format(count))

    set_blogs_to_published.short_description = 'Mark selected blogs as published'


admin.site.register(Blog, BlogAdmin)
