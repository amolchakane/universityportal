from django.urls import path, include

from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='homepage'),
    path('register', views.register, name='register'),
    path('article/new/', views.article_new, name='article_new'),
    path('article/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('details/<int:id>/', views.article_details, name='details'),
    path('approve/<int:pk>/', views.article_approve, name='approve'),
    path('article/<int:pk>/comment/', views.add_comment_to_article, name='add_comment_to_article'),
]
