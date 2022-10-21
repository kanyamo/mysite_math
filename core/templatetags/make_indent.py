from atexit import register
from django import template
import json
register = template.Library()

@register.filter
def make_indent(s, n):
    """json形式の文字列sをスペースn個単位でインデントして整形する"""
    return json.dumps(json.loads(s), indent=4, ensure_ascii=False)
