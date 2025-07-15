from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, FormView

from webapp.forms import ArticleForm

from webapp.models import Article


class ArticleListView(View):

    def get(self, request):
        articles = Article.objects.order_by('-created_at')
        return render(request, 'articles/index.html', {"articles": articles})


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
