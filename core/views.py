from django.shortcuts import redirect, render
from django.views import generic
from .models import Article
from .forms import create_article_edit_form


# Create your views here.
class BaseTemplateView(generic.TemplateView):  # base.htmlで使うコンテキストを取得
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_articles'] = Article.objects.all().order_by('view_count').reverse()[:3]  # 人気記事上位3件を取得
        context['new_articles'] = Article.objects.all().order_by('pub_date').reverse()[:3]  # 最新記事3件を取得
        return context

class IndexView(BaseTemplateView):  # ホーム表示
    template_name = 'core/index.html'

class ArticleDetailView(BaseTemplateView):
    template_name = 'core/article_detail.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Article.objects.get(pk=pk)
        obj.view_count += 1
        obj.save()
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        article = Article.objects.get(pk=pk)
        context['article'] = article
        return context

class ArticleCreateView(BaseTemplateView):
    template_name = 'core/article_edit.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = create_article_edit_form()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        length = request.POST.get('length', default=0)
        count = 1
        while request.POST.get(f'content{count}'):
            pass
        return redirect('index')

class ArticleEditView(BaseTemplateView):  # CreateViewと違い、オブジェクトの情報を取得してからそれをコンテキストに渡す
    template_name = 'core/article_edit.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')

