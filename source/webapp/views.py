from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import ArticleForm
# from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404

from webapp.models import Article
from webapp.validation import validate


class IndexView(View):

    def get(self, request):
        articles = Article.objects.order_by('-created_at')
        return render(request, 'index.html', {"articles": articles})


class CreateView(View):

    def post(self, request):
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            author = form.cleaned_data.get('author')
            status = form.cleaned_data.get('status')
            tags = form.cleaned_data.get('tags')
            article = Article.objects.create(title=title, content=content, author=author, status=status)
            article.tags.set(tags)
            return redirect("article-detail", pk=article.pk)
        else:
            return render(request, 'create_article.html', {"form": form})

    def get(self, request):
        form = ArticleForm()
        return render(request, 'create_article.html', context={"form": form})


def update_article(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article.title = form.cleaned_data.get('title')
            article.content = form.cleaned_data.get('content')
            article.author = form.cleaned_data.get('author')
            article.status = form.cleaned_data.get('status')
            article.save()
            article.tags.set(form.cleaned_data.get('tags'))
            return redirect("article-detail", pk=article.pk)
        else:
            return render(request, 'update_article.html', {"form": form})
    else:
        form = ArticleForm(initial={
            "title": article.title,
            "content": article.content,
            "author": article.author,
            "status": article.status,
            "tags": article.tags.all()
        })
        return render(request, 'update_article.html', {"form": form})


def delete_article(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.delete()
        return redirect("index")
    else:
        return render(request, 'delete_article.html', {"article": article})


class DetailView(TemplateView):
    # template_name = 'detail_article.html'
    def dispatch(self, request, *args, **kwargs):
        self.article = get_object_or_404(Article, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.article
        return context

    def get_template_names(self):
        if self.article.status == "deleted":
            return ["deleted_article.html"]
        else:
            return ['detail_article.html']


