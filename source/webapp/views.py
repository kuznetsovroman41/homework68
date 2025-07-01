from django.shortcuts import render, redirect, get_object_or_404

from webapp.forms import ArticleForm
# from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404

from webapp.models import Article
from webapp.validation import validate


# Create your views here.
def index(request):
    articles = Article.objects.order_by('-created_at')
    return render(request, 'index.html', {"articles": articles})


def create_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            author = form.cleaned_data.get('author')
            status = form.cleaned_data.get('status')
            article = Article.objects.create(title=title, content=content, author=author, status=status)
            return redirect("article-detail", pk=article.pk)
        else:
            return render(request, 'create_article.html', {"form": form})
    else:
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
            return redirect("article-detail", pk=article.pk)
        else:
            return render(request, 'update_article.html', {"form": form})
    else:
        form = ArticleForm(initial={
            "title": article.title,
            "content": article.content,
            "author": article.author,
            "status": article.status,
        })
        return render(request, 'update_article.html', {"form": form})

def delete_article(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.delete()
        return redirect("index")
    else:
        return render(request, 'delete_article.html', {"article": article})


def detail_article(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'detail_article.html', {"article": article})

