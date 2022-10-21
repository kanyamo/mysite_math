// ページ読み込み時のアニメーションを防ぐ
document.addEventListener('DOMContentLoaded', () => {
    window.setTimeout(() => {
        const body = document.getElementById('body');
        body.classList.remove('preload');
    }, 300);
});