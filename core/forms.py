from django import forms
from .models import Article
from django_editorjs_fields import EditorJsWidget

class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'thumbnail', 'content', 'category']
        widgets = {
            'content': EditorJsWidget(
                config={'minHeight': 300},
                plugins=[
                    "@editorjs/header",
                    "@editorjs/image",
                    "@editorjs/code@2.6.0",  # version allowed :)
                    "@editorjs/list@latest",
                    "@editorjs/inline-code",
                    "@editorjs/table",
                    "editorjs-math@1.0.2/dist/bundle.js",
                ],
                tools={
                    "math": {
                        'class': 'MathTex',
                    }
                }
            ),
        }
