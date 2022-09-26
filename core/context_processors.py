from django.http import HttpRequest
from .models import Article, Category
from django.conf import settings
import os

def base_template_context_processor(request: HttpRequest):
    return {
        'root_categories': Category.objects.filter(is_root=True),  # ルートカテゴリたちを持ってくる
        'popular_articles': Article.objects.filter(is_published=True).order_by('view_count').reverse()[:3],  # 人気記事上位3件を取得
        'new_articles': Article.objects.filter(is_published=True).order_by('pub_date').reverse()[:3],  # 最新記事3件を取得
        'DEBUG': settings.DEBUG
    }