from django.urls import path

from webapp.views import UpdateArticleView, delete_article, ArticleListView, CreateArticleView, DetailArticleView

urlpatterns = [
    path('', ArticleListView.as_view(), name='index'),
    path('add-article/', CreateArticleView.as_view(), name='add-article'),
    path('article/<int:pk>/', DetailArticleView.as_view(), name='article-detail'),

    path('article/<int:pk>/update/', UpdateArticleView.as_view(), name='article-update'),

    path('article/<int:pk>/delete/', delete_article, name='article-delete'),
]
