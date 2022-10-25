from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator
from django_editorjs_fields import EditorJsTextField
from django.conf import settings
import json
import textwrap  # html整形のため
import re # パラグラフやリストの中にhtml要素を記述するため

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
    # contentとcontent_as_htmlを分けることで、記事の読み込み時にいちいちjsonからパースする必要がなくなる
    # 通常はcontentを編集し、その内容を自動的にcontent_as_htmlに書き出す
    content = EditorJsTextField(verbose_name='内容',blank=True)
    content_as_html = models.TextField('内容のHTML', max_length=1000000, null=False, blank=True, default='', help_text='html要素からは編集しないでください。このフィールドの変更は自動制御されているので、上書きされます。htmlを編集したい場合、editor.jsのraw要素を使ってください。')

    def __str__(self):
        return self.title

    def compose_html(self):
        """EditorJsTextFieldをHTMLにする"""
        content = json.loads(self.content)
        result = ''

        def list_to_html(depth, dict_list):
            if dict_list:
                result = '\t' * (2 * depth - 3) + f'<{"ol" if depth == 2 else "ul"} class="toc-{"ol" if depth == 2 else "ul"} level{depth}">\n'
                index = 0
                n = len(dict_list)
                while index < n:
                    result += '\t' * (2 * depth - 2) + '<li class="toc-li">\n'
                    result += '\t' * (2 * depth - 1) + f'<a href="#{dict_list[index]["id"]}" class="toc-a">{dict_list[index]["data"]["text"]}</a>' + '\n'
                    index += 1
                    sub_list = []
                    while index < n and dict_list[index]['data']['level'] != depth:
                        sub_list += [dict_list[index]]
                        index += 1
                    result += list_to_html(depth + 1, sub_list)
                    result += '\t' * (2 * depth - 2) + '</li>\n'
                result += "\t" * (2 * depth - 3) + f'</{"ol" if depth == 2 else "ul"}>\n'
                return result
            return ''
        
        if self.has_table_of_contents:
            headers = list(filter(lambda block: block['type'] == 'Header', content['blocks']))
            toc = list_to_html(2, headers)
            result += f'<div class="toc-container">\n\t<p class="toc-title">Contents</p>\n{toc}</div>\n'
        for block in content['blocks']:
            element = ''
            match block['type']:
                case 'Header':
                    element = f"""
                    <h{block['data']['level']} id="{block['id']}">
                        {block['data']['text']}
                    </h{block['data']['level']}>
                    """
                case 'Image':
                    element = f"""
                    <figure>
                        <img class="content-image" src="{block['data']['file']['url']}">
                        <figcaption class="content-image-caption">
                            {block['data']['caption']}
                        </figcaption>
                    </figure>
                    """
                case 'Math':
                    element = f"""
                    <div class="equation-container">
                        \\[{block['data']['text']}\\]
                    </div>
                    """
                case 'paragraph':
                    element = f"""
                    <p>{block['data']['text']}</p>
                    """
                case 'List':
                    class_name = 'ol' if block['data']['style'] == 'ordered' else 'ul'
                    element = f'\n<{class_name}>\n'
                    for item in block['data']['items']:
                        element += f'\t<li>{item}</li>\n'
                    element += f'</{class_name}>\n'
                case 'Code':
                    # pre要素の内部なので整形困難
                    element = f'\n<blockquote><pre><code class="code">{block["data"]["code"]}</code></pre></blockquote>\n'
                case 'Raw':
                    element = '\n<div class="raw-html-container">\n'
                    for line in block['data']['html'].splitlines():
                        element += f'\t{line}\n'
                    element += '</div>\n'
                case 'Table':
                    data = block['data']['content']
                    element = '\n<table class="article-table">\n'
                    for row in range(len(data)):
                        element += f'\t<tr>\n'
                        for column in range(len(data[row])):
                            element += f'\t\t<td>{data[row][column]}</td>\n'
                        element += f'\t</tr>\n'
                    element += '</table>\n'
                case 'Checklist':
                    element = '\n<ul class="checklist">\n'
                    for item in block['data']['items']:
                        element += f'\t<li checked="{item["checked"]}">{item["text"]}</li>\n'
                    element += '</ul>\n'
                case 'Delimiter':
                    element = f"""
                    <hr class="delimiter">
                    """
                case 'Quote':
                    element = f"""
                    <div>
                        <blockquote class="quote">{block['data']['text']}</blockquote>
                        <p class="quote-caption">{block['data']['caption']}</p>
                    </div>
                    """
                case 'Warning':
                    element = f"""
                    <div class="warning-container">
                        <p class="warning-title">
                            <i class="fa-solid fa-triangle-exclamation"></i>
                            {block['data']['title']}</p>
                        <div class="warning-message">
                            {block['data']['message']}
                        </div>
                    </div>
                    """
                case 'LinkTool':
                    element = f"""
                    <a class="external-link-block" href="{block['data']['link']}">
                        <div class="external-link-title">
                            <i class="fa-solid fa-arrow-up-right-from-square"></i>
                            {block['data']['meta']['title']}
                        </div>
                        <p class="external-link-description">
                            {block['data']['meta']['description']}
                        </p>
                        <span class="external-link-url">
                            {block['data']['link']}
                        </span>
                    </a>
                    """
                case _ as str:
                    element = f"""
                    <p style="color: red;">規定のタイプ以外の要素が検出されました：{str}</p>
                    """
            result += textwrap.dedent(element)[:-1]  # 一番浅いインデントを0にして、最後の改行を削除
        exp = r'&lt;(.{1,5})&gt;'
        self.content_as_html = re.sub(exp, r'<\1>', result)
        # セーブは行わないので、compose_htmlを実行した後セーブする必要がある
