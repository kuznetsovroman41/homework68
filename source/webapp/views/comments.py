from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView

from webapp.forms.comments import CommentForm
from webapp.models import Article, Comment


class CreateCommentView(CreateView):
    form_class = CommentForm
    template_name = "comments/create_comment.html"

    # def form_valid(self, form):
    #     article = get_object_or_404(Article, pk=self.kwargs['pk'])
    #     comment = form.save(commit=False)
    #     comment.article = article
    #     comment.save()
    #     return redirect("article-detail", pk=article.pk)

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        form.instance.article = article
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse("article-detail", kwargs={"pk": self.object.article_id})


class UpdateCommentView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/update_comment.html"


    # def get_success_url(self):
    #     return reverse("article-detail", kwargs={"pk": self.object.article_id})


class DeleteCommentView(DeleteView):
    model = Comment

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.delete(request, *args, **kwargs)


    def get_success_url(self):
        return self.object.get_absolute_url()