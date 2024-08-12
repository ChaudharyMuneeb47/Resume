document.addEventListener("DOMContentLoaded", function () {
    const portfolioItems = document.querySelectorAll('.portfolio-item');

    portfolioItems.forEach(item => {
        item.addEventListener('click', () => {
            item.querySelector('.portfolio-content').classList.toggle('show');
        });
    });
});
window.addEventListener('scroll', function() {
    var header = document.querySelector('header');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});
