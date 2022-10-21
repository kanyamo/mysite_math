document.addEventListener('DOMContentLoaded', () => {
    // KaTeX読み込み
    renderMathInElement(document.body, {delimiters: [
        {left: "\\[", right: "\\]", display: true},
        {left: "$", right: "$", display: false}
    ]});

    // TikZJax遅延読み込み
    var tz = document.createElement('script');
    tz.type = 'text/javascript';
    tz.src = 'https://tikzjax.com/v1/tikzjax.js';
    document.head.appendChild(tz);

    // パースしたJSONデータを文字列化し、preタグの中に入れ込む
    // KaTeX読み込みより遅くすることで数式化を防ぐ
    let pre = document.getElementById("article-json-data");
    if (pre != null){
        pre.innerText = JSON.stringify(content, undefined, 4);
    }
});