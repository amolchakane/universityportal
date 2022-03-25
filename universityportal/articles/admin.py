from django.contrib import admin

# Register your models here.
from .models import Articles, UserRoles, Comment


class ArticleAdmin(admin.ModelAdmin):
    """ArticleAdmin class for adding options on Django admin front
    This will be used further while registering Articles model
    """
    list_display = ('title', 'status', 'user', 'reviewer', 'created_at')
    list_filter = ("status",)
    search_fields = ['title', 'body']
    prepopulated_fields = {'body': ('title',)}


class UserRoleAdmin(admin.ModelAdmin):
    """UserRoleAdmin class for adding options in Django admin front end"""
    list_display = ('role', 'user')
    list_filter = ("role",)


class CommentAdmin(admin.ModelAdmin):
    """CommentAdmin class for adding options in Django admin front end"""
    list_display = ('text', 'get_article_name', 'author', 'created_at')
    search_fields = ['text', 'author']

    def get_article_name(self, obj):
        return obj.article.title
    get_article_name.admin_order_field = 'article'  #Allows column order sorting
    get_article_name.short_description = 'Article Title'  #Renames column head


"""Register all the custom models using the classes created above into the Django Admin"""
admin.site.register(Articles, ArticleAdmin)
admin.site.register(UserRoles, UserRoleAdmin)
admin.site.register(Comment, CommentAdmin)
