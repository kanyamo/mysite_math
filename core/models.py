from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator
from django_editorjs import EditorJsField

alphanumeric = RegexValidator(r'^[0-9a-zA-Z_]*$', '半角英数字とアンダースコアのみ使用可能です。')  # 内部カテゴリ名として半角英数字とアンダースコアしか使えないようにする

# Create your models here.
class MyUser(AbstractUser):
    # usernameとemailはすでにAbstractUserで定義済み,passwordはすでにAbstractBaseUserで定義済み
    icon = models.ImageField('アイコン画像', upload_to='icons/', default='default/default_user_icon.png')
    pub_date = models.DateTimeField('登録日', default=timezone.now)
    display_name = models.CharField('表示名', max_length=100, default='表示名')


class Category(models.Model):
    upper = models.ForeignKey('self', verbose_name='上位カテゴリ', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('カテゴリ名', max_length=100, unique=True)
    inner_name = models.CharField('内部的カテゴリ名', max_length=100, validators=[alphanumeric], unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    thumbnail = models.ImageField('サムネイル画像', upload_to='thumbnails/%Y/%m/%d/', default='default/default_thumbnail.png')
    pub_date = models.DateTimeField('投稿日', default=timezone.now)
    renew_date = models.DateTimeField('更新日', default=timezone.now)
    title = models.CharField('タイトル', max_length=200)
    view_count = models.IntegerField('PV数', default=0)  # 約21億が上限。さすがにそこまではいかないだろう
    category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.SET_DEFAULT, default=1)  # もしカテゴリーが削除されると、HOMEカテゴリ(id=1)に強制的に属させる
    author = models.ForeignKey(MyUser, verbose_name='作者', on_delete=models.SET_DEFAULT, default=1)  # 作者が削除されると、記事はすべて管理者(id=1)のものになる
    content = EditorJsField(verbose_name='内容', editorjs_config={
        'tools': {
            'Image': {
                'config': {
                    'endpoints': {
                        'byFile': '/imageUPLoad/',
                        'byUrl': '/imageUPLoad/',
                    },
                    'additionalRequestHeaders': [{'Content-Type': 'multipart/form-data'}]
                }
            },
            'Attaches': {
                'config': {
                    'endpoint': '/fileUPLoad/'
                }
            },
            'header': {
                'class': 'Header',
                'config': {
                    'placeholder': '見出しを入力...',
                    'levels': [2, 3, 4, 5, 6]
                }
            }
        }
    })

    def __str__(self):
        return self.title


