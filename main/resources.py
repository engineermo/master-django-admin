from import_export import resources
from main.models import Comment


class CommenResource(resources.ModelResource):
    class Meta:
        model = Comment
