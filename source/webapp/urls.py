from django.urls import path

from webapp.views import UpdateArticleView, DeleteArticleView, ArticleListView, CreateArticleView, DetailArticleView, like_views
from webapp.views.comments import CreateCommentView, UpdateCommentView, DeleteCommentView

app_name = 'webapp'

#webapp:index
urlpatterns = [
    path('', ArticleListView.as_view(), name='index'),
    path('add-article/', CreateArticleView.as_view(), name='add-article'),
    path('article/<int:pk>/', DetailArticleView.as_view(), name='article-detail'),
    path('article/<int:pk>/update/', UpdateArticleView.as_view(), name='article-update'),
    path('article/<int:pk>/delete/', DeleteArticleView.as_view(), name='article-delete'),

    path('article/<int:pk>/add-comment/', CreateCommentView.as_view(), name='add-comment'),
    path('comment/<int:pk>/update/', UpdateCommentView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', DeleteCommentView.as_view(), name='comment-delete'),
    path('article/<int:article_id>/like/', like_views.toggle_article_like, name='article_like'),
    path('comment/<int:comment_id>/like/', like_views.toggle_comment_like, name='comment_like'),
]
