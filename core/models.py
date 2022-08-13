from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')  # 内部カテゴリ名として半角英数字しか使えないようにする

# Create your models here.
class MyUser(AbstractUser):
    # usernameとemailはすでにAbstractUserで定義済み,passwordはすでにAbstractBaseUserで定義済み
    icon = models.ImageField('アイコン画像', upload_to='icons/', default='default/default_user_icon.png')
    pub_date = models.DateTimeField('登録日', default=timezone.now)

class Category(models.Model):
    upper = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('カテゴリ名', max_length=100)
    inner_name = models.CharField('内部的カテゴリ名', max_length=100, validators=[alphanumeric])

    def __str__(self):
        return self.name


class Article(models.Model):
    length = models.IntegerField('長さ')
    thumbnail = models.ImageField('サムネイル画像', upload_to='thumbnails/%Y/%m/%d/', default='default/default_thumbnail.png')
    pub_date = models.DateTimeField('投稿日', default=timezone.now)
    renew_date = models.DateTimeField('更新日', default=timezone.now)
    title = models.CharField('タイトル', max_length=200)
    view_count = models.IntegerField('PV数', default=0)  # 約21億が上限。さすがにそこまではいかないだろう
    # category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=Category.objects.get(inner_name='home'))  # もしカテゴリーが削除されると、HOMEカテゴリに強制的に属させる
    # author = models.ForeignKey(MyUser, on_delete=models.SET_DEFAULT, default=MyUser.objects.get(username='admin'))  # 作者が削除されると、記事はすべて管理者のものになる

    def __str__(self):
        return self.title

class Content(models.Model):
    list_number = models.IntegerField('順番')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.article}({self.list_number})'

class Headline(models.Model):
    text = models.CharField('見出し', max_length=200)
    CHOICE_SIZE = ((2, 2), (3, 3), (4, 4), (5, 5), (6, 6))
    size = models.IntegerField('階層', choices=CHOICE_SIZE)
    content = models.OneToOneField(Content, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.content}:{self.text}'

class Paragraph(models.Model):
    paragraph = models.TextField('文章')
    content = models.OneToOneField(Content, on_delete=models.CASCADE)

    def __str__(self):
        paragraph = self.paragraph
        if len(paragraph) > 20:
            paragraph = paragraph[:20] + '...'
        return f'{self.content}:{paragraph}'

class Image(models.Model):
    image = models.ImageField('画像', upload_to='images/%Y/%m/%d/', default='default/default_image.png')
    content = models.OneToOneField(Content, on_delete=models.PROTECT)  # 下位カテゴリがあると削除できない
    alt = models.CharField('説明', max_length=200, default='画像')

    def __str__(self):
        return f'{self.content}:{self.alt}'

