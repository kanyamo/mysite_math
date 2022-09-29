function isHeightViewable(element){
    const {top, bottom} = element.getBoundingClientRect();
    return top >= 0 && bottom <= window.innerHeight;
}

document.addEventListener('DOMContentLoaded', () => {
    marks = document.querySelectorAll('mark');
    window.addEventListener('scroll', () => {
        marks.forEach(mark => {
            if (isHeightViewable(mark) && !mark.classList.contains('active')) {
                mark.classList.add('active');
            }
        });
    });
});