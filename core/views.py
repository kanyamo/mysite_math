from django.shortcuts import render
from django.views import generic
from .models import MyUser, Article, Content, Headline, Paragraph, Image

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'core/index.html'

class ArticleDetailView(generic.DetailView):
    template_name = 'core/article_detail.html'  # 自動でこの名前が検索されるので不要ではある
    context_object_name = 'article'
    model = Article

    def get_object(self):  # PV数カウントのため
        obj = super().get_object()
        obj.view_count += 1
        obj.save()
        return obj
