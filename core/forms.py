from django import forms
from .models import Article, Category, MyUser
from django_editorjs_fields import EditorJsWidget
from django.conf import settings

class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'thumbnail', 'content', 'category', 'has_table_of_contents', 'is_published', 'lead']
        widgets = {
            'content': EditorJsWidget(
                config={'minHeight': 300}
            ),
        }


class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['upper', 'name', 'inner_name', 'description', 'is_root']
    
    def clean_upper(self):
        # データベースには保存せずに、モデルのオブジェクトを取得
        # viewでインスタンスを編集元に指定しているので、pkを取得できる
        default_pk = self.save(commit=False).pk
        category = self.cleaned_data['upper']
        i = 0  # 無限ループを防止するための変数
        while i < 100 and category is not None:
            i += 1
            pk = category.pk
            if pk == default_pk:
                raise forms.ValidationError('カテゴリ木がループしています。カテゴリのグラフは有向木である必要があります。')
            category = category.upper
        return self.cleaned_data['upper']
        


class UserEditForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['icon', 'username', 'display_name', 'description']
