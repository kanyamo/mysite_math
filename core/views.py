from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from .models import Article, Category
from .forms import ArticleEditForm, CategoryEditForm
from django.utils import timezone

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
        while category is not None:
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
            return render(request, self.template_name, {'form':form, 'creating_new': True})
    
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
            article.has_table_of_contents = form.cleaned_data['has_table_of_contents']
            article.renew_date = timezone.localtime(timezone.now())  # 更新時には投稿日やビュー数、著者は更新しない
            article.save()
            return redirect('core:detail', pk=article.pk)
        else:
            return render(request, self.template_name, {'form':form, 'pk': pk, 'creating_new': False})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        context['pk'] = article.pk
        context['form'] = ArticleEditForm(instance=article)
        context['creating_new'] = False  # テンプレートを共有しているので必要になってくる
        return context

class CategoryCreateView(generic.TemplateView):
    template_name = 'core/category_edit.html'

    def post(self, request):
        form = CategoryEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:index')
        else:
            return render(request, self.template_name, {'form':form, 'creating_new': True})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CategoryEditForm()
        context['creating_new'] = True
        return context

class CategoryDetailView(generic.TemplateView):
    template_name = 'core/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inner_name = self.kwargs.get('inner_name')  # 内部カテゴリ名をurlのサブディレクトリとして用いる
        category = get_object_or_404(Category, inner_name=inner_name)
        context['category'] = category
        context['lower_categories'] = category.lowers.all()
        context['articles'] = category.article_set.all()
        category_list = []
        while category is not None:
            category_list.append(category)
            category = category.upper
        category_list.reverse()  # 上位カテゴリを後ろに加えていったので最後にreverse
        context['category_list'] = category_list
        return context

class CategoryEditView(generic.TemplateView):
    template_name = 'core/category_edit.html'

    def post(self, request, inner_name):
        category = Category.objects.get(inner_name=inner_name)
        form = CategoryEditForm(request.POST, instance=category)
        if form.is_valid():
            category.name = form.cleaned_data['name']
            category.inner_name = form.cleaned_data['inner_name']
            category.upper = form.cleaned_data['upper']
            category.description = form.cleaned_data['description']
            category.is_root = form.cleaned_data['is_root']
            category.save()
            return redirect('core:category-detail', inner_name=category.inner_name)
        else:
            return render(request, self.template_name, {'form':form, 'inner_name': inner_name, 'creating_new': False})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, inner_name=self.kwargs.get('inner_name'))
        context['inner_name'] = category.inner_name
        context['form'] = CategoryEditForm(instance=category)
        context['creating_new'] = False
        return context

