from django.contrib import admin
from .models import MyUser, Article, Category

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Article)
admin.site.register(Category)
