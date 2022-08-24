from django import forms
from .models import Article
from django_editorjs_fields import EditorJsWidget

class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'thumbnail', 'content', 'category']
        widgets = {
            'content': EditorJsWidget(config={'minHeight': 300}),
        }
