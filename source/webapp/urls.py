from django.urls import path

from webapp.views import index, create_article, detail_article, update_article, delete_article

urlpatterns = [
    path('', index, name='index'),
    path('add-article/', create_article, name='add-article'),
    path('article/<int:pk>/', detail_article, name='article-detail'),

    path('article/<int:pk>/update/', update_article, name='article-update'),

    path('article/<int:pk>/delete/', delete_article, name='article-delete'),



]
