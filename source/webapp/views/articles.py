from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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


class CreateArticleView(CreateView):
    template_name = 'articles/create_article.html'
    # model = Article
    # fields = ['title', 'author', 'content', 'tags']
    form_class = ArticleForm


class UpdateArticleView(UpdateView):
    template_name = 'articles/update_article.html'
    form_class = ArticleForm
    model = Article



class DeleteArticleView(DeleteView):
    model = Article
    template_name = 'articles/delete_article.html'
    success_url = reverse_lazy('index')



class DetailArticleView(DetailView):
    template_name = 'articles/detail_article.html'
    model = Article


    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result['comments'] = self.object.comments.order_by('-created_at')
        return result
