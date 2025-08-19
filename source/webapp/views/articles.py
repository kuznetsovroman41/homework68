from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.models.like import CommentLike
from webapp.forms import ArticleForm, SearchForm
from webapp.models import Article


class ArticleListView(ListView):
    template_name = 'articles/index.html'
    model = Article
    context_object_name = "articles"
    ordering = ['-created_at']
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        print(request.user)
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(
                Q(title__icontains=self.search_value) |
                Q(author__icontains=self.search_value)
            )

        if self.request.user.is_authenticated:
            for article in queryset:
                article.is_liked_by_user = article.likes.filter(user=self.request.user).exists()

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        result = super().get_context_data(**kwargs)
        result['search_form'] = self.form
        if self.search_value:
            result["query"] = urlencode({"search": self.search_value})
            result['search'] = self.search_value
        return result

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

class CreateArticleView(LoginRequiredMixin, CreateView):
    template_name = 'articles/create_article.html'
    # model = Article
    # fields = ['title', 'author', 'content', 'tags']
    form_class = ArticleForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateArticleView(PermissionRequiredMixin ,UpdateView):
    template_name = 'articles/update_article.html'
    form_class = ArticleForm
    model = Article

    permission_required = 'webapp.change_article'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    # def dispatch(self, request, *args, **kwargs):
    #     user = request.user
    #     if not user.is_authenticated:
    #         return redirect('webapp:index')
    #     if not user.has_perm('webapp.change_article'):
    #         raise PermissionDenied
    #     return super().dispatch(request, *args, **kwargs)


class DeleteArticleView(PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = 'articles/delete_article.html'
    success_url = reverse_lazy('webapp:index')

    permission_required = "webapp.delete_article"

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

class DetailArticleView(DetailView):
    template_name = 'articles/detail_article.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.object.comments.order_by('-created_at')

        if self.request.user.is_authenticated:
            for comment in comments:
                comment.is_liked_by_user = CommentLike.objects.filter(
                    comment=comment,
                    user=self.request.user
                ).exists()
                comment.likes_count = CommentLike.objects.filter(comment=comment).count()

        context['comments'] = comments
        return context
