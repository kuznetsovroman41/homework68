from django.shortcuts import render
from django.http import HttpResponseRedirect

from webapp.articles_db import ArticlesDB


# Create your views here.
def index(request):
    articles = ArticlesDB.articles
    ArticlesDB.set_new_avatar()
    cat_avatar = ArticlesDB.cat_avatar
    return render(request, 'index.html', {"articles": articles, "cat_avatar": cat_avatar})


def create_article(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author')

        article = {
            'title': title,
            'content': content,
            'author': author
        }
        ArticlesDB.articles.append(article)
        return HttpResponseRedirect("/")
    else:
        return render(request, 'create_article.html')
