from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django.db.models import Count
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from rangefilter.filter import DateTimeRangeFilter
from leaflet.admin import LeafletGeoAdmin
from import_export.admin import ImportExportModelAdmin
from .resources import CommenResource

# Register your models here.
from django.utils import timezone

from .models import Blog, Comment, Category, Place


class CommentInline(admin.StackedInline):
    model = Comment
    fields = ('text', 'is_active')
    extra = 1
    classes = ('collapse',)  # --> to collapse this section in the django admin


class CategoryInline(admin.StackedInline):
    model = Category
    fields = ('name', 'is_active')
    extra = 1
    classes = ('collapse',)


class BlogAdmin(SummernoteModelAdmin):
    list_display = (
        'title', 'date_created', 'last_modified', 'is_draft', 'days_since_creation', 'no_of_comments', 'show_category')
    list_filter = ('is_draft', 'date_created',
                   ('date_created', DateTimeRangeFilter),)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 10
    actions = ('set_blogs_to_published',)
    date_hierarchy = 'date_created'
    # fields = (('title', 'slug'), 'body', 'is_draft')

    fieldsets = (
        (None, {
            'fields': (('title', 'slug'), 'body'),

        }),
        ('Advanced options', {
            # notice categories is another model but since it has a many to many to relationship with blog model it
            # should be added here
            'fields': ('is_draft', 'categories'),
            'description': 'Options to configure blog creations',
            # TODO: this is to collapse the Advanced options field while adding a blog
            'classes': ('collapse',)
        }),
    )

    summernote_fields = ('body',)
    # below is only valid for Foreign Key Models
    inlines = (CommentInline,)
    filter_horizontal = ('categories',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        try:
            del actions['delete_selected']
        except:
            pass
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        """
        this is used to extend the queryset
        in our case we will use annotate --> to add the number of comments in our blog
        :param request:
        :return:
        """
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(comments_count=Count('comments'))
        return queryset

    def no_of_comments(self, blog):
        """
        display the number of comments to add to list display
        :param blog:
        :return: blog.no_of_comments
        """
        return blog.comments_count

    def show_category(self, obj):
        """
        display the category in the blog' section
        :param blog:
        :return:
        """
        return "\n" + ", ".join([c.name for c in obj.categories.all()])

    no_of_comments.admin_order_field = 'comments_count'

    def days_since_creation(self, Blog):
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


class CommentAdmin(ImportExportModelAdmin):
    list_display = ('blog', 'text', 'date_created', 'is_active')
    # list_editable = ('text', 'is_active', ) # to edit within admin
    list_per_page = 10
    list_filter = (
        ('blog', RelatedDropdownFilter),
    )
    resource_class = CommenResource
    list_select_related = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_active',
    )


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Place, LeafletGeoAdmin)
