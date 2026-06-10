const inventariVenible = [
    { id: 'peix_llobarro', nom: 'Llobarro', preu: 100, estoc: 4 },
    { id: 'peix_carpa', nom: 'Carpa', preu: 30, estoc: 12 },
    { id: 'cultiu_xirivia', nom: 'Xirivia', preu: 35, estoc: 20 },
    { id: 'cultiu_patata', nom: 'Patata', preu: 80, estoc: 5 },
    { id: 'plat_amanida', nom: 'Amanida', preu: 110, estoc: 2 },
    { id: 'plat_truita', nom: 'Truita al forn', preu: 150, estoc: 1 }
];

let articlesVendaFiltrats = [];
let cistellaVenda = {};
let paginaVenda = 1;
const itemsPerPaginaVenda = 5;

const btnVendre = document.getElementById('btn-vendre');
const modalVendre = document.getElementById('modal-vendre');
const llistaVenda = document.getElementById('llista-venda');
const totalVendaEl = document.getElementById('total-venda');
const textPaginacioVenda = document.getElementById('text-paginacio-venda');

btnVendre.addEventListener('click', obrirVenda);

function obrirVenda() {
    cistellaVenda = {};
    paginaVenda = 1;
    inventariVenible.forEach(a => cistellaVenda[a.id] = 0);
    articlesVendaFiltrats = [...inventariVenible];
    document.getElementById('cercador-venda').value = '';
    modalVendre.style.display = 'flex';
    renderitzarVenda();
    actualitzarTotalVenda();
}

function tancarModalVendre() {
    modalVendre.style.display = 'none';
}

function cercarVenda() {
    const text = document.getElementById('cercador-venda').value.toLowerCase();
    articlesVendaFiltrats = inventariVenible.filter(a => a.nom.toLowerCase().includes(text));
    paginaVenda = 1;
    renderitzarVenda();
}

function canviarPaginaVenda(direccio) {
    const maxPagines = Math.ceil(articlesVendaFiltrats.length / itemsPerPaginaVenda) || 1;
    paginaVenda += direccio;
    if (paginaVenda < 1) paginaVenda = 1;
    if (paginaVenda > maxPagines) paginaVenda = maxPagines;
    renderitzarVenda();
}

function renderitzarVenda() {
    llistaVenda.innerHTML = '';
    const maxPagines = Math.ceil(articlesVendaFiltrats.length / itemsPerPaginaVenda) || 1;
    textPaginacioVenda.innerText = `Pàgina ${paginaVenda} / ${maxPagines}`;

    const inici = (paginaVenda - 1) * itemsPerPaginaVenda;
    const fi = inici + itemsPerPaginaVenda;
    const articlesPagina = articlesVendaFiltrats.slice(inici, fi);

    articlesPagina.forEach(article => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${article.nom} <br><small style="font-size: 16px;">(Tenim: ${article.estoc})</small></td>
            <td>${article.preu}G</td>
            <td>
                <div class="control-quantitat">
                    <button class="btn-quantitat" onclick="canviarQuantitatVenda('${article.id}', -1)">-</button>
                    <input type="number" id="qv-${article.id}" class="input-quantitat" value="${cistellaVenda[article.id]}" min="0" max="${article.estoc}" onchange="inputQuantitatVenda('${article.id}', ${article.estoc})">
                    <button class="btn-quantitat" onclick="canviarQuantitatVenda('${article.id}', 1)">+</button>
                </div>
            </td>
        `;
        llistaVenda.appendChild(tr);
    });
}

function canviarQuantitatVenda(id, canvi) {
    const article = inventariVenible.find(a => a.id === id);
    let actual = parseInt(document.getElementById(`qv-${id}`).value) || 0;
    let nova = actual + canvi;
    if (nova < 0) nova = 0;
    if (nova > article.estoc) nova = article.estoc;
    document.getElementById(`qv-${id}`).value = nova;
    cistellaVenda[id] = nova;
    actualitzarTotalVenda();
}

function inputQuantitatVenda(id, max) {
    let val = parseInt(document.getElementById(`qv-${id}`).value) || 0;
    if (val < 0) val = 0;
    if (val > max) val = max;
    document.getElementById(`qv-${id}`).value = val;
    cistellaVenda[id] = val;
    actualitzarTotalVenda();
}

function actualitzarTotalVenda() {
    let total = 0;
    inventariVenible.forEach(article => {
        total += (cistellaVenda[article.id] || 0) * article.preu;
    });
    totalVendaEl.innerText = total;
}

function confirmarVenda() {
    tancarModalVendre();
}
