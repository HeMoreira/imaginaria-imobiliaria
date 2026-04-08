const plantasCarrosselTrack = document.getElementById("plantasCarrosselTrack");
if (plantasCarrosselTrack) {
    const plantasCarrosselTotal = document.querySelectorAll(".plantas-carrossel-slide").length;
    let plantasCarrosselAtual = 0;

    function plantasCarrosselMover(dir) {
        plantasCarrosselAtual = (plantasCarrosselAtual + dir + plantasCarrosselTotal) % plantasCarrosselTotal;
        plantasCarrosselTrack.style.transform = `translateX(-${plantasCarrosselAtual * 100}%)`;
    }

    document.querySelector(".plantas-carrossel-btn.prev").addEventListener("click", () => plantasCarrosselMover(-1));
    document.querySelector(".plantas-carrossel-btn.next").addEventListener("click", () => plantasCarrosselMover(1));
}