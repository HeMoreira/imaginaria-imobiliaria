const container1 = document.getElementById('multiple-image-form');
const container2 = document.getElementById('multiple-plant-form');
const btnAdd1 = document.getElementById('add-new-image');
const btnAdd2 = document.getElementById('add-new-plant');
const btnRemove1 = document.getElementById('remove-last-image')
const btnRemove2 = document.getElementById('remove-last-plant')

function AdicionarNovaImagemComContexto(container) {
    const index = container.querySelectorAll('.image-group').length;
    
    const newGroup = document.createElement('div');
    newGroup.className = 'image-group';
    newGroup.innerHTML = `
        <br>
        <label>Imagem</label>
        <input type="file" name="items-${index}-image" required>
        <label>Descrição</label>
        <input type="text" name="items-${index}-description" required>
    `;
    container.append(newGroup);
}
function RemoverUltimaImagemComContexto(container) {
    const index = (container.querySelectorAll('.image-group').length)-1;
    const ultimo_elemento = container.querySelectorAll('.image-group')[index]
    ultimo_elemento.remove()
}

btnAdd1.addEventListener('click', () => {
    AdicionarNovaImagemComContexto(container1)
});

btnAdd2.addEventListener('click', () => {
    AdicionarNovaImagemComContexto(container2)
});

btnRemove1.addEventListener('click', () => {
    RemoverUltimaImagemComContexto(container1)
});

btnRemove2.addEventListener('click', () => {
    RemoverUltimaImagemComContexto(container2)
});