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


class UserEditForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['icon', 'username', 'display_name', 'description']
