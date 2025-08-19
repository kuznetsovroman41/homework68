from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from webapp.models.article import Article
from webapp.models.comment import Comment
from webapp.models.like import ArticleLike, CommentLike


@login_required
def toggle_article_like(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    like, created = ArticleLike.objects.get_or_create(article=article, user=request.user)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    likes_count = article.likes.count()

    return JsonResponse({'likes_count': likes_count, 'liked': liked})


@login_required
def toggle_comment_like(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    likes_count = comment.likes.count()

    return JsonResponse({'likes_count': likes_count, 'liked': liked})

