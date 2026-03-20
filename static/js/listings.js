const buttons = document.querySelectorAll('.filter-btn');

const slides = document.querySelector('.carousel-slides');
const btnEsq = document.querySelector('.carousel-btn--left');
const btnDir = document.querySelector('.carousel-btn--right');
const cards = document.querySelectorAll('.card');
let visible_cards = document.querySelectorAll('.card[style="display: block;"]');

let totalCards = cards.length-3;
let pot_slide = 0;
let index = 0;
let timer = 0;

cards.forEach(card => {
    card.style.display = "block";
});

buttons.forEach(button => {
    button.addEventListener('click', () => {
        buttons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        
        let filter = button.getAttribute('data-filter');

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
    });
});
function updateSlidePower() {
    visible_cards = document.querySelectorAll('.card[style="display: block;"]');
    if (window.innerWidth <= 600) {
        totalCards = visible_cards.length;
        pot_slide = -index * 100.35;
    } else if (window.innerWidth <= 900) {
        totalCards = visible_cards.length-1;
        pot_slide = -index * 51.5;
    } else {
        totalCards = visible_cards.length-2;
        pot_slide = -index * 33.85;
    }
}
function moverSlide() {
    updateSlidePower();
    slides.style.transform = `translateX(${pot_slide}%)`;
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