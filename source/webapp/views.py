from django.shortcuts import render
from django.http import HttpResponseRedirect

from webapp.models import Article


# Create your views here.
def index(request):
    articles = Article.objects.order_by('-created_at')
    return render(request, 'index.html', {"articles": articles})


def create_article(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author')
        Article.objects.create(title=title, content=content, author=author)
        return HttpResponseRedirect("/")
    else:
        return render(request, 'create_article.html')


def article_detail(request, *args, pk, **kwargs):
    print(args)
    print(kwargs)
    if pk:
        try:
            article = Article.objects.get(id=pk)
            return render(request, 'detail_article.html', {"article": article})
        except Article.DoesNotExist:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")
