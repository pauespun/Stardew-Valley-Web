let llavorsBotiga = [];
let llavorsFiltrades = [];
let cistella = {};
let paginaBotiga = 1;
const itemsPerPaginaBotiga = 5;

const btnBotiga = document.getElementById('btn-botiga');
const modalBotiga = document.getElementById('modal-botiga');
const llistaLlavors = document.getElementById('llista-llavors');
const totalCompraEl = document.getElementById('total-compra');
const textPaginacioBotiga = document.getElementById('text-paginacio-botiga');

btnBotiga.addEventListener('click', obrirBotiga);

function obrirBotiga() {
    cistella = {};
    paginaBotiga = 1;
    document.getElementById('cercador-llavors').value = '';
    modalBotiga.style.display = 'flex';

    fetch(URL_LLISTAR_LLAVORS)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            llavorsBotiga = data.llavors;
            llavorsBotiga.forEach(l => cistella[l.id] = 0);
            llavorsFiltrades = [...llavorsBotiga];

            renderitzarBotiga();
            actualitzarTotal();
        });
}

function tancarModalBotiga() {
    modalBotiga.style.display = 'none';
}

function cercarLlavors() {
    const text = document.getElementById('cercador-llavors').value.toLowerCase();
    llavorsFiltrades = llavorsBotiga.filter(l => l.nom.toLowerCase().includes(text));
    paginaBotiga = 1;
    renderitzarBotiga();
}

function canviarPaginaBotiga(direccio) {
    const maxPagines = Math.ceil(llavorsFiltrades.length / itemsPerPaginaBotiga) || 1;
    paginaBotiga += direccio;
    if (paginaBotiga < 1) paginaBotiga = 1;
    if (paginaBotiga > maxPagines) paginaBotiga = maxPagines;
    renderitzarBotiga();
}

function renderitzarBotiga() {
    llistaLlavors.innerHTML = '';
    const maxPagines = Math.ceil(llavorsFiltrades.length / itemsPerPaginaBotiga) || 1;
    textPaginacioBotiga.innerText = `Pàgina ${paginaBotiga} / ${maxPagines}`;

    const inici = (paginaBotiga - 1) * itemsPerPaginaBotiga;
    const fi = inici + itemsPerPaginaBotiga;
    const llavorsPagina = llavorsFiltrades.slice(inici, fi);

    llavorsPagina.forEach(llavor => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${llavor.nom}</td>
            <td>${llavor.preu}G</td>
            <td>
                <div class="control-quantitat">
                    <button class="btn-quantitat" onclick="canviarQuantitat('${llavor.id}', -1)">-</button>
                    <input type="number" id="q-${llavor.id}" class="input-quantitat" value="${cistella[llavor.id]}" min="0" onchange="inputQuantitat('${llavor.id}')">
                    <button class="btn-quantitat" onclick="canviarQuantitat('${llavor.id}', 1)">+</button>
                </div>
            </td>
        `;
        llistaLlavors.appendChild(tr);
    });
}

function canviarQuantitat(id, canvi) {
    let actual = parseInt(document.getElementById(`q-${id}`).value) || 0;
    let nova = actual + canvi;
    if (nova < 0) nova = 0;
    document.getElementById(`q-${id}`).value = nova;
    cistella[id] = nova;
    actualitzarTotal();
}

function inputQuantitat(id) {
    let val = parseInt(document.getElementById(`q-${id}`).value) || 0;
    if (val < 0) val = 0;
    document.getElementById(`q-${id}`).value = val;
    cistella[id] = val;
    actualitzarTotal();
}

function actualitzarTotal() {
    let total = 0;

    llavorsBotiga.forEach(llavor => {
        total += (cistella[llavor.id] || 0) * llavor.preu;
    });

    totalCompraEl.innerText = total;
}

function confirmarCompra() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(URL_COMPRAR_LLAVORS, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({
            cistella: cistella
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        const diners = document.getElementById("diners");
        if (diners) {
            diners.innerText = data.diners;
        }

        tancarModalBotiga();
    });
}