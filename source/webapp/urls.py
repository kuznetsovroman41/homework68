from django.urls import path

from webapp.views import UpdateView, delete_article, IndexView, CreateView, DetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('add-article/', CreateView.as_view(), name='add-article'),
    path('article/<int:pk>/', DetailView.as_view(), name='article-detail'),

    path('article/<int:pk>/update/', UpdateView.as_view(), name='article-update'),

    path('article/<int:pk>/delete/', delete_article, name='article-delete'),



]
