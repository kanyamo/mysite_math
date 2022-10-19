document.addEventListener('DOMContentLoaded', () => {
    window.setTimeout(() => {
        const body = document.getElementById('body');
        body.classList.remove('preload');
    }, 100);
});