from django.contrib import admin

# Register your models here.
from .models import Articles, UserRoles


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'reviewer', 'created_at')
    list_filter = ("status",)
    search_fields = ['title', 'body']
    prepopulated_fields = {'body': ('title',)}


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('role', 'user')
    list_filter = ("role",)


admin.site.register(Articles, ArticleAdmin)
admin.site.register(UserRoles, UserRoleAdmin)
