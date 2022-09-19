from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator
from django_editorjs_fields import EditorJsTextField
from django.conf import settings

alphanumeric = RegexValidator(r'^[0-9a-zA-Z_]*$', '半角英数字とアンダースコアのみ使用可能です。')  # 内部カテゴリ名として半角英数字とアンダースコアしか使えないようにする

def local_now():
    return timezone.localtime(timezone.now())

class MyUser(AbstractUser):
    # usernameとemailはすでにAbstractUserで定義済み,passwordはすでにAbstractBaseUserで定義済み
    icon = models.ImageField('アイコン画像', upload_to='icons/', default='default/default_user_icon.png')
    pub_date = models.DateTimeField('登録日', default=local_now)
    display_name = models.CharField('表示名', max_length=100, default='表示名')


class Category(models.Model):
    upper = models.ForeignKey('self', verbose_name='上位カテゴリ', on_delete=models.CASCADE, blank=True, null=True, related_name='lowers')
    name = models.CharField('カテゴリ名', max_length=100, unique=True)
    inner_name = models.CharField('内部的カテゴリ名', max_length=100, validators=[alphanumeric], unique=True)
    description = models.TextField('カテゴリの説明文', blank=False, null=False, default='これがカテゴリの説明文です。')
    is_root = models.BooleanField('ルートカテゴリかどうか', default=False)  # ルートカテゴリはもっとも上位のカテゴリであることを示す

    def __str__(self):
        return self.name


class Article(models.Model):
    thumbnail = models.ImageField('サムネイル画像', upload_to='thumbnails/%Y/%m/%d/', default='default/default_thumbnail.png')
    pub_date = models.DateTimeField('投稿日', default=local_now)
    renew_date = models.DateTimeField('更新日', default=local_now)
    title = models.CharField('タイトル', max_length=200)
    view_count = models.IntegerField('PV数', default=0)  # 約21億が上限。さすがにそこまではいかないだろう
    category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.SET_DEFAULT, default=1)  # もし属するカテゴリーが削除されると、HOMEカテゴリ(id=1)に強制的に属させる
    author = models.ForeignKey(MyUser, verbose_name='作者', on_delete=models.SET_DEFAULT, default=1)  # 作者が削除されると、記事はすべて管理者(id=1)のものになる
    content = EditorJsTextField()

    def __str__(self):
        return self.title


