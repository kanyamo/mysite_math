from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django.views.decorators.csrf import requires_csrf_token
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.conf import settings
from .models import Article, Category
from .forms import ArticleEditForm
from django.utils import timezone
import os

class IndexView(generic.TemplateView):  # ホーム表示
    template_name = 'core/index.html'

class ArticleDetailView(generic.TemplateView):
    template_name = 'core/article_detail.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Article, pk=pk)
        obj.view_count += 1
        obj.save()
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        context['article'] = article
        # 親が存在しない地点までさかのぼってカテゴリーのリストを作成する
        category = article.category
        category_list = []
        while not category is None:
            category_list.append(category)
            category = category.upper
        category_list.reverse()  # 上位カテゴリを後ろに加えていったので最後にreverse
        context['category_list'] = category_list
        return context

class ArticleCreateView(generic.TemplateView):
    template_name = 'core/article_edit.html'

    def post(self, request):
        form = ArticleEditForm(request.POST, request.FILES)
        if form.is_valid:
            post = form.save(commit=False)
            post.pub_date = timezone.localtime(timezone.now())
            post.renew_date = timezone.localtime(timezone.now())
            post.view_count = 0
            post.author = request.user
            post.save()
            return redirect('core:index')
        else:
            pass
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ArticleEditForm()
        context['creating_new'] = True  # テンプレートを共有しているので必要になってくる
        return context

class ArticleEditView(generic.TemplateView):
    template_name = 'core/article_edit.html'

    def post(self, request, pk):
        article=Article.objects.get(pk=pk)
        form = ArticleEditForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            if form.cleaned_data['thumbnail']:
                article.thumbnail = form.cleaned_data['thumbnail']
            article.content = form.cleaned_data['content']
            article.renew_date = timezone.localtime(timezone.now())  # 更新時には投稿日やビュー数、著者は更新しない
            article.save()
            return redirect('core:detail', pk=article.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        context['pk'] = article.pk
        context['form'] = ArticleEditForm(instance=article)
        context['creating_new'] = False  # テンプレートを共有しているので必要になってくる
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
