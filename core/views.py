from django.shortcuts import render
from django.views import generic
from .models import MyUser, Article, Content, Headline, Paragraph, Image

# Create your views here.
class BaseTemplateView(generic.TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_articles'] = Article.objects.all().order_by('view_count')

class IndexView(BaseTemplateView):
    template_name = 'core/index.html'

class ArticleDetailView(BaseTemplateView):
    template_name = 'core/article_detail.html'  # 自動でこの名前が検索されるので不要ではある
    context_object_name = 'article'
    model = Article

    def get_object(self):  # PV数カウントのため
        obj = super().get_object()
        obj.view_count += 1
        obj.save()
        return obj
