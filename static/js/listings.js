const buttons = document.querySelectorAll('.filter-btn');

const slides = document.querySelector('.carousel-slides');
const cards = document.querySelectorAll('.card');
const btnEsq = document.querySelector('.carousel-btn--left');
const btnDir = document.querySelector('.carousel-btn--right');

let totalCards = (cards.length-1)/2 | 0;
let index = 0;
let timer = 0;

buttons.forEach(button => {
    button.addEventListener('click', () => {
        let filter = button.getAttribute('data-filter');
        const cards = document.querySelectorAll('.card');

        buttons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        cards.forEach(card => {
            card_type = card.querySelector('.card-type');
            const category = card_type.getAttribute('data-category');

            if (filter === "ALL" || category === filter) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
        index = 0;
        moverSlide();
        totalCards = (document.querySelectorAll('.card[style="display: block;"]').length-1)/2 | 0;
    });
});
function moverSlide() {
    slides.style.transform = `translateX(${-index * 55}%)`;
    timer = 0;
}
btnDir.addEventListener('click', () => {
    index = (index + 1) % totalCards;
    moverSlide();
});
btnEsq.addEventListener('click', () => {
    index = (index - 1 + totalCards) % totalCards;
    moverSlide();
});
setInterval(() => {
    timer++;
    if(timer >= 5){
        index = (index + 1) % totalCards;
        moverSlide();
    }
}, 1000);