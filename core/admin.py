from django.contrib import admin
from .models import MyUser, Article, Content, Headline, Paragraph, Image

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Article)
admin.site.register(Content)
admin.site.register(Headline)
admin.site.register(Paragraph)
admin.site.register(Image)
