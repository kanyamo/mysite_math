from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.
class MyUser(AbstractUser):
    # usernameとemailはすでにAbstractUserで定義済み,passwordはすでにAbstractBaseUserで定義済み
    icon = models.ImageField('アイコン画像', upload_to='icons/', default='default/default_user_icon.png')
    pub_date = models.DateTimeField('登録日', default=timezone.now)

class Article(models.Model):
    length = models.IntegerField('長さ')
    thumbnail = models.ImageField('サムネイル画像', upload_to='thumbnails/%Y/%m/%d/', default='default/default_thumbnail.png')
    pub_date = models.DateTimeField('投稿日', default=timezone.now)
    renew_date = models.DateTimeField('更新日', default=timezone.now)
    title = models.CharField('タイトル')

class Content(models.Model):
    list_number = models.IntegerField('順番')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

class Headline(models.Model):
    text = models.CharField('見出し')
    size = models.IntegerChoices('階層')
    content = models.OneToOneField(Content, on_delete=models.CASCADE)

class Paragraph(models.Model):
    paragraph = models.TextField('文章')
    content = models.OneToOneField(Content, on_delete=models.CASCADE)

class Image(models.Model):
    image = models.ImageField('画像', upload_to='images/%Y/%m/%d/', default='default/default_image.png')
    content = models.OneToOneField(Content, on_delete=models.CASCADE)

