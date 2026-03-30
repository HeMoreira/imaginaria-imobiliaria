const lista_imagens = document.querySelectorAll(".form-imagem-adicional");
const lista_plantas = document.querySelectorAll(".form-imagem-plantas");
const btnAdd1 = document.getElementById('add-new-image');
const btnAdd2 = document.getElementById('add-new-plant');
const btnRemove1 = document.getElementById('remove-last-image')
const btnRemove2 = document.getElementById('remove-last-plant')

imagensField = document.querySelectorAll(".form-imagem-adicional")
imagensField.forEach(field => {
    field.style.display = "none";
});
plantasField = document.querySelectorAll(".form-imagem-plantas")
plantasField.forEach(field => {
    field.style.display = "none";
});

function AdicionarNovaImagemComContexto(listaFields) {
    c = 0;
    listaFields.forEach(field => {
        if (field.style.display == "none" && c <= 0){
            field.style.display = "block";
            c++;
        }
    });
}
function RemoverUltimaImagemComContexto(listaFields) {
    let c = 0;
    [...listaFields].reverse().forEach(field => {
        if (field.style.display !== "none" && c < 1) {
            field.style.display = "none";
            c++;
        }
    });
}

btnAdd1.addEventListener('click', () => {
    AdicionarNovaImagemComContexto(lista_imagens)
});

btnAdd2.addEventListener('click', () => {
    AdicionarNovaImagemComContexto(lista_plantas)
});

btnRemove1.addEventListener('click', () => {
    RemoverUltimaImagemComContexto(lista_imagens)
});

btnRemove2.addEventListener('click', () => {
    RemoverUltimaImagemComContexto(lista_plantas)
});