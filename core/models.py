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
    description = models.TextField('自己紹介文', max_length=2000, default='これが作者の紹介文です。')
    def __str__(self):
        return self.display_name


class Category(models.Model):
    upper = models.ForeignKey('self', verbose_name='上位カテゴリ', on_delete=models.PROTECT, blank=True, null=True, related_name='lowers')  # 上位カテゴリは、そのカテゴリに属するカテゴリを全て削除しない限り削除できない
    name = models.CharField('カテゴリ名', max_length=100, unique=True)
    inner_name = models.CharField('内部カテゴリ名', max_length=100, validators=[alphanumeric], unique=True)
    description = models.TextField('カテゴリの説明文', blank=False, null=False, default='これがカテゴリの説明文です。')
    is_root = models.BooleanField('ナビゲーションに表示するかどうか', default=False, help_text='最上位のカテゴリは必ず表示する必要があります。')  # ルートカテゴリは大きいカテゴリであることを示す

    def __str__(self):
        return self.name


class Article(models.Model):
    thumbnail = models.ImageField('サムネイル画像', upload_to='thumbnails/%Y/%m/%d/', default='default/default_thumbnail.png')
    pub_date = models.DateTimeField('投稿日', default=local_now)
    renew_date = models.DateTimeField('更新日', default=local_now)
    title = models.CharField('タイトル', max_length=200)
    view_count = models.IntegerField('PV数', default=0)  # 約21億が上限。さすがにそこまではいかないだろう
    category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.PROTECT, default=1)  # カテゴリは、そのカテゴリに属する記事を全て削除しない限り削除できない
    author = models.ForeignKey(MyUser, verbose_name='作者', on_delete=models.SET_DEFAULT, default=1)  # 作者が削除されると、記事はすべて管理者(id=1)のものになる
    lead = models.TextField('リード文', max_length=2000, blank=True, default='', help_text='投稿日や作者の直後で目次（表示する場合）の直前に挿入される文章です。リード文は記事のリンクにも使われます。')
    has_table_of_contents = models.BooleanField('目次を表示するかどうか', default=False)
    is_published = models.BooleanField('公開するかどうか', default=True)
    content = EditorJsTextField()

    def __str__(self):
        return self.title


