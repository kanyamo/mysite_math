from django import forms

class ArticleEditForm(forms.Form):
    pass

def create_article_edit_form():
    form =  ArticleEditForm()
    return form