from django.shortcuts import redirect, render
from django.views import generic
from django.views.decorators.csrf import requires_csrf_token
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.conf import settings
from .models import Article
from .forms import ArticleEditForm
from django.utils import timezone
import os


class BaseTemplateView(generic.TemplateView):  # base.htmlで使うコンテキストを取得
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_articles'] = Article.objects.all().order_by('view_count').reverse()[:3]  # 人気記事上位3件を取得
        context['new_articles'] = Article.objects.all().order_by('pub_date').reverse()[:3]  # 最新記事3件を取得
        context['base_url'] = os.getenv('BASE_URL')  # ローカルでは127.0.0.1:8000, デプロイ環境ではhttps://math.kanyamo.com
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

    def post(self, request):
        form = ArticleEditForm(request.POST, request.FILES)
        if form.is_valid:
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.renew_date = timezone.now()
            post.view_count = 0
            post.author = request.user
            post.save()
            return redirect('core:index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ArticleEditForm()
        return context

@requires_csrf_token
def upload_image_view(request):
    f = request.FILES['image']
    path_string = f'images/{timezone.localtime(timezone.now()).year}/{str(timezone.localtime(timezone.now()).month).zfill(2)}/{str(timezone.localtime(timezone.now()).day).zfill(2)}'
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, path_string), base_url=os.path.join(settings.MEDIA_URL, path_string))
    filename = str(f)
    file = fs.save(filename, f)
    file_url = fs.url(file)
    return JsonResponse({'success': 1, 'file': {'url': file_url}})

@requires_csrf_token
def upload_file_view(request):
    f = request.FILES['file']
    path_string = f'files/{str(timezone.localtime(timezone.now()).year).zfill(2)}/{str(timezone.localtime(timezone.now()).month).zfill(2)}'
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, path_string), base_url=os.path.join(settings.MEDIA_URL, path_string))
    filename = str(f)
    file = fs.save(filename, f)
    file_url = fs.url(file)
    return JsonResponse({
        'success': 1,
        'file': {
            'url': file_url,
            'size': fs.size(filename),
            'name': str(f)
            }
        })
