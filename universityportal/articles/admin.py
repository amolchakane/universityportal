from django.contrib import admin

# Register your models here.
from .models import Articles, UserRoles, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'user', 'reviewer', 'created_at')
    list_filter = ("status",)
    search_fields = ['title', 'body']
    prepopulated_fields = {'body': ('title',)}


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('role', 'user')
    list_filter = ("role",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'get_article_name', 'author', 'created_at')
    search_fields = ['text', 'author']

    def get_article_name(self, obj):
        return obj.article.title
    get_article_name.admin_order_field = 'article'  #Allows column order sorting
    get_article_name.short_description = 'Article Title'  #Renames column head


admin.site.register(Articles, ArticleAdmin)
admin.site.register(UserRoles, UserRoleAdmin)
admin.site.register(Comment, CommentAdmin)
