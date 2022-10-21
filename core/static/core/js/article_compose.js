document.addEventListener('DOMContentLoaded', () => {
    // KaTeX読み込み
    // preの中はレンダリングされない（多分）
    renderMathInElement(document.body, {delimiters: [
        {left: "\\[", right: "\\]", display: true},
        {left: "$", right: "$", display: false}
    ]});

    // tikzJax遅延読み込み
    var tz = document.createElement('script');
    tz.type = 'text/javascript';
    tz.src = 'https://tikzjax.com/v1/tikzjax.js';
});