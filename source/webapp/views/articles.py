from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView, FormView, ListView

from webapp.forms import ArticleForm, SearchForm

from webapp.models import Article


class ArticleListView(ListView):
    template_name = 'articles/index.html'
    model = Article
    context_object_name = "articles"
    ordering = ['-created_at']
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(Q(title__icontains=self.search_value) | Q(author__icontains=self.search_value))
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


class CreateArticleView(FormView):
    template_name = 'articles/create_article.html'
    form_class = ArticleForm

    def form_valid(self, form):
        article = form.save()
        return redirect("article-detail", pk=article.pk)


class UpdateArticleView(FormView):
    template_name = 'articles/update_article.html'
    form_class = ArticleForm

    def dispatch(self, request, *args, **kwargs):
        self.article = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Article, pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.article
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.article
        return context

    def form_valid(self, form):
        form.save()
        return redirect("article-detail", pk=self.article.pk)


def delete_article(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.delete()
        return redirect("index")
    else:
        return render(request, 'articles/delete_article.html', {"article": article})


class DetailArticleView(TemplateView):
    template_name = 'articles/detail_article.html'

    def dispatch(self, request, *args, **kwargs):
        self.article = get_object_or_404(Article, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.article
        return context

    # def get_template_names(self):
    #     if self.article.status == "deleted":
    #         return ["deleted_article.html"]
    #     else:
    #         return ['detail_article.html']
