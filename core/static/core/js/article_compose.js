function unescapeUnicode(string) {
    return string.replace(/\\u([a-fA-F0-9]{4})/g, function(matchedString, group1) {
        return String.fromCharCode(parseInt(group1, 16));
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const articleContent = document.getElementById('article-content');
    const re = /&lt;(.{1,5})&gt;/g;  // htmlタグをエスケープから戻して表示されるようにする
    const s = document.getElementById('article-content-data');
    const jsonString = unescapeUnicode(s.textContent).replace(re, '<$1>');
    const content = JSON.parse(jsonString);
    const blocks = content.blocks;
    for (let index = 0; index < blocks.length; index++ ){
        switch(blocks[index].type){  // JSONファイルを展開し、そのブロックの各タイプごとに適した処理でブロックを追加する
            case 'Header':
                let head = document.createElement(`h${blocks[index].data.level}`);
                head.textContent = blocks[index].data.text;
                head.setAttribute('id', blocks[index].id);
                articleContent.appendChild(head);
                break;
            case 'Image':
                let figure = document.createElement('figure');
                let image = document.createElement('img');
                let image_caption = document.createElement('figcaption');
                image.classList.add('content-image');
                image_caption.classList.add('content-image-caption');
                image.src = `${blocks[index].data.file.url}`;
                image_caption.textContent = blocks[index].data.caption;
                figure.appendChild(image);
                figure.appendChild(image_caption);
                articleContent.appendChild(figure);
                break;
            case 'Math':
                let math_div = document.createElement('div');
                math_div.classList.add('equation-container');
                math_div.innerHTML = '\\[' + blocks[index].data.text + '\\]';
                articleContent.appendChild(math_div);
                break;
            case 'paragraph':
                let p = document.createElement('p');
                p.innerHTML = blocks[index].data.text;
                articleContent.appendChild(p);
                break;
            case 'List':
                if (blocks[index].data.style == 'unordered') {
                    list = document.createElement('ul');
                } else {
                    list = document.createElement('ol');
                }
                for (const item in blocks[index].data.items) {
                    let li = document.createElement('li');
                    li.innerHTML = blocks[index].data.items[item];
                    list.appendChild(li);
                }
                articleContent.appendChild(list);
                break;
            case 'Code':
                let blockquote = document.createElement('blockquote');
                let pre = document.createElement('pre');
                let code = document.createElement('code');
                code.textContent = blocks[index].data.code;
                code.classList.add('code');
                pre.appendChild(code);
                blockquote.appendChild(pre);
                articleContent.appendChild(blockquote);
                break;
            case 'Raw':
                let container = document.createElement('div');
                container.classList.add('raw_html_container');
                container.innerHTML = blocks[index].data.html;
                articleContent.append(container);
                break;
            case 'Table':
                let table = document.createElement('table');
                let data = blocks[index].data.content;
                table.classList.add('article-table');
                let trs = [];
                let tds = [];
                for (let row = 0; row < data.length; row++){
                    tds = [];
                    trs.push(document.createElement('tr'));
                    for (let column = 0; column < data.length; column++){
                        tds.push(document.createElement('td'));
                        tds[column].textContent = data[row][column];
                        trs[row].appendChild(tds[column]);
                    table.appendChild(trs[row]);
                    }
                articleContent.appendChild(table);
                }
                break;
            case 'Checklist':
                let checklist_ul = document.createElement('ul');
                checklist_ul.classList.add('checklist')
                for (const item in blocks[index].data.items) {
                    let li = document.createElement('li');
                    li.innerHTML = blocks[index].data.items[item].text;
                    li.setAttribute('checked', blocks[index].data.items[item].checked);
                    checklist_ul.appendChild(li);
                }
                articleContent.appendChild(checklist_ul);
                break;
            case 'Delimiter':
                let hr = document.createElement('hr');
                hr.classList.add('delimiter');
                articleContent.appendChild(hr);
                break;
            case 'Quote':
                let blockQuote_container = document.createElement('div');
                let blockQuote = document.createElement('blockquote');
                let quote_caption = document.createElement('p');
                blockQuote.classList.add('quote');
                quote_caption.classList.add('quote-caption');
                blockQuote.innerHTML = blocks[index].data.text;
                quote_caption.innerHTML = blocks[index].data.caption;
                blockQuote_container.appendChild(blockQuote);
                blockQuote_container.appendChild(quote_caption);
                articleContent.appendChild(blockQuote_container);
                break;
            case 'Warning':
                let warning_div = document.createElement('div');
                warning_div.classList.add('warning-container');
                let warning_title = document.createElement('p');
                warning_title.classList.add('warning-title');
                let warning_i = document.createElement('i');
                warning_i.classList.add("fa-solid", "fa-triangle-exclamation");
                let warning_message = document.createElement('p');
                warning_message.classList.add('warning-message');
                warning_title.innerHTML = " " + blocks[index].data.title;
                warning_message.innerHTML = blocks[index].data.message;
                warning_title.prepend(warning_i);
                warning_div.appendChild(warning_title);
                warning_div.appendChild(warning_message);
                articleContent.appendChild(warning_div);
                break;
            case 'LinkTool':
                let link_container = document.createElement('a');
                link_container.setAttribute('href', blocks[index].data.link);
                link_container.classList.add('external-link-block');
                let link_title = document.createElement('div');
                link_title.classList.add('external-link-title');
                link_title.textContent = " " + blocks[index].data.meta.title;
                let link_i = document.createElement('i');
                link_i.classList.add("fa-solid", "fa-arrow-up-right-from-square");
                let link_description = document.createElement('p');
                link_description.classList.add('external-link-description');
                link_description.textContent = blocks[index].data.meta.description;
                let link_url = document.createElement('span');
                link_url.classList.add('external-link-url');
                link_url.textContent = blocks[index].data.link;
                link_title.prepend(link_i);
                link_container.appendChild(link_title);
                link_container.appendChild(link_description);
                link_container.appendChild(link_url);
                articleContent.appendChild(link_container);
        }
    }

    // h2見出しを抽出し、目次を作成する
    let toc_ol = document.getElementById('toc-ol')
    if (toc_ol != null){
        let h2_headers = blocks.filter((block) => {
            return block.type == 'Header' && block.data.level == 2;
        });
        for (let index = 0; index < h2_headers.length; index++ ){
            let a = document.createElement('a');
            a.classList.add('toc-a');
            a.setAttribute('href', '#' + h2_headers[index].id)
            let li = document.createElement('li');
            li.classList.add('toc-li');
            a.textContent = h2_headers[index].data.text;
            li.appendChild(a);
            toc_ol.appendChild(li);
        }
    }

    renderMathInElement(document.body, {delimiters: [
        {left: "\\[", right: "\\]", display: true},
        {left: "$", right: "$", display: false}
    ]});  // KaTeX読み込み

    var tz = document.createElement('script');
    tz.type = 'text/javascript';
    tz.src = 'https://tikzjax.com/v1/tikzjax.js';
    document.head.appendChild(tz);  // TikZJax遅延読み込み

    // パースしたJSONデータを文字列化し、preタグの中に入れ込む
    // KaTeX読み込みより遅くすることで数式化を防ぐ
    let pre = document.getElementById("article-json-data");
    if (pre != null){
        pre.innerText = JSON.stringify(content, undefined, 4);
    }
});