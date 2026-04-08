let carrossel_list = [{}];
carrossel_list[0]["carrossel"] = document.querySelector('.imoveis.id1');
if (document.querySelector('.imoveis.id2')) {
    carrossel_list[1] = {};
    carrossel_list[1]["carrossel"] = document.querySelector('.imoveis.id2');
}

for (let i = 0; i < carrossel_list.length; i++) {
    carrossel_list[i]["buttons"] = carrossel_list[i]["carrossel"].querySelectorAll('.filter-btn');
    carrossel_list[i]["cards"] = carrossel_list[i]["carrossel"].querySelectorAll('.card');
    
    carrossel_list[i]["slides"] = carrossel_list[i]["carrossel"].querySelector('.carousel-slides');
    carrossel_list[i]["btnEsq"] = carrossel_list[i]["carrossel"].querySelector('.carousel-btn--left');
    carrossel_list[i]["btnDir"] = carrossel_list[i]["carrossel"].querySelector('.carousel-btn--right');
    carrossel_list[i]["visible_cards"] = carrossel_list[i]["carrossel"].querySelectorAll('.card[style="display: block;"]');

    carrossel_list[i]["totalCards"] = carrossel_list[i]["cards"].length-3;
    carrossel_list[i]["pot_slide"] = 0;
    carrossel_list[i]["index"] = 0;
    carrossel_list[i]["timer"] = 0;
}

let all_cards = document.querySelectorAll('.card');
all_cards.forEach(card => {
    card.style.display = "block";
    for (let i = 0; i < carrossel_list.length; i++) {
        moverSlide(i);
    }
});

function updateOnClickFilters(indice) {
    carrossel_list[indice]["buttons"].forEach(button => {
        button.addEventListener('click', () => {
            carrossel_list[indice]["buttons"].forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            let filter = button.getAttribute('data-filter');

            carrossel_list[indice]["cards"].forEach(card => {
                card_type = card.querySelector('.card-type');
                const category = card_type.getAttribute('data-category');

                if (filter === "ALL" || category === filter) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            });
            carrossel_list[indice]["index"] = 0;
            moverSlide(indice);
        });
    });
}
for (let i = 0; i < carrossel_list.length; i++) {
    updateOnClickFilters(i);
}

function updateSlidePower(indice) {
    const visible_cards = carrossel_list[indice]["carrossel"].querySelectorAll('.card[style="display: block;"]');
    if (window.innerWidth <= 600) {
        carrossel_list[indice]["totalCards"] = visible_cards.length;
        carrossel_list[indice]["pot_slide"] = -carrossel_list[indice]["index"] * 100.35;
    } else if (window.innerWidth <= 900) {
        carrossel_list[indice]["totalCards"] = visible_cards.length-1;
        carrossel_list[indice]["pot_slide"] = -carrossel_list[indice]["index"] * 51.5;
    } else {
        carrossel_list[indice]["totalCards"] = visible_cards.length-2;
        carrossel_list[indice]["pot_slide"] = -carrossel_list[indice]["index"] * 33.85;
    }
}
function moverSlide(indice) {
    updateSlidePower(indice);
    carrossel_list[indice]["slides"].style.transform = `translateX(${carrossel_list[indice]["pot_slide"]}%)`;
    carrossel_list[indice]["timer"] = 0;
}
for (let i = 0; i < carrossel_list.length; i++) {
    carrossel_list[i]["btnDir"].addEventListener('click', () => {
        carrossel_list[i]["index"] = (carrossel_list[i]["index"] + 1) % carrossel_list[i]["totalCards"];
        moverSlide(i);
    });
    carrossel_list[i]["btnEsq"].addEventListener('click', () => {
        carrossel_list[i]["index"] = (carrossel_list[i]["index"] - 1 + carrossel_list[i]["totalCards"]) % carrossel_list[i]["totalCards"];
        moverSlide(i);
    });
}
setInterval(() => {
    for (let i = 0; i < carrossel_list.length; i++) {
        carrossel_list[i]["timer"]++;
        if(carrossel_list[i]["timer"] >= 5){
            carrossel_list[i]["index"] = (carrossel_list[i]["index"] + 1) % carrossel_list[i]["totalCards"];
            moverSlide(i);
        }
    }
}, 1000);