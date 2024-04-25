function isHeightViewable(element) {
    const { top, bottom } = element.getBoundingClientRect();
    return top >= 0 && bottom <= window.innerHeight;
}

function activateViewableElement(element) {
    if (isHeightViewable(element) && !element.classList.contains('active')) {
        element.classList.add('active');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    marks = document.querySelectorAll('mark');
    marks.forEach(mark => {
        activateViewableElement(mark);
    });
    window.addEventListener('scroll', () => {
        marks.forEach(mark => {
            activateViewableElement(mark);
        });
    });
});
