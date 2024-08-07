document.addEventListener("DOMContentLoaded", function () {
    const portfolioItems = document.querySelectorAll('.portfolio-item');

    portfolioItems.forEach(item => {
        item.addEventListener('click', () => {
            item.querySelector('.portfolio-content').classList.toggle('show');
        });
    });
});
