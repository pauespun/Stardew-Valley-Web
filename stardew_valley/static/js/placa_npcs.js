let npcs = [];
let paginaActual = 1;
const itemsPerPagina = 6;
let npcSeleccionat = null;

const modalNpcs = document.getElementById('modal-npcs');
const modalObjectes = document.getElementById('modal-objectes');
const llistaNpcs = document.getElementById('llista-npcs');
const textPaginacio = document.getElementById('text-paginacio');
const btnRegalarPrincipal = document.getElementById('btn-regalar-principal');
const btnPrev = document.getElementById('btn-prev');
const btnNext = document.getElementById('btn-next');
const titolModalObjectes = document.getElementById('titol-modal-objectes');
const llistaObjectesRegal = document.getElementById('llista-objectes-regal');

btnRegalarPrincipal.addEventListener('click', obrirModalNpcs);
btnPrev.addEventListener('click', () => canviarPagina(-1));
btnNext.addEventListener('click', () => canviarPagina(1));

function obrirModalNpcs() {
    paginaActual = 1;
    modalNpcs.style.display = 'flex';

    fetch(URL_LLISTAR_NPCS)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            npcs = data.npcs;
            renderitzarNpcs();
        });
}

function tancarModalNpcs() {
    modalNpcs.style.display = 'none';
}

function renderitzarNpcs() {
    llistaNpcs.innerHTML = '';

    const totalPagines = Math.ceil(npcs.length / itemsPerPagina) || 1;
    const inici = (paginaActual - 1) * itemsPerPagina;
    const fi = inici + itemsPerPagina;
    const npcsPagina = npcs.slice(inici, fi);

    npcsPagina.forEach(npc => {
        const targeta = document.createElement('div');
        targeta.className = 'targeta-npc';
        targeta.innerHTML = `
            <div class="info-npc">
                <strong>${npc.nom}</strong><br>
                🎂 ${npc.aniversari}
            </div>
            <button class="boto-acció" onclick="obrirModalObjectes(${npc.id}, '${npc.nom}')">Regalar</button>
        `;
        llistaNpcs.appendChild(targeta);
    });

    textPaginacio.innerText = `Pàgina ${paginaActual} / ${totalPagines}`;
}

function canviarPagina(direccio) {
    const totalPagines = Math.ceil(npcs.length / itemsPerPagina) || 1;

    paginaActual += direccio;

    if (paginaActual < 1) paginaActual = 1;
    if (paginaActual > totalPagines) paginaActual = totalPagines;

    renderitzarNpcs();
}

function obrirModalObjectes(idNpc, nomNpc) {
    npcSeleccionat = idNpc;
    titolModalObjectes.innerText = `Regalar a ${nomNpc}`;

    modalNpcs.style.display = 'none';
    modalObjectes.style.display = 'flex';

    fetch(URL_LLISTAR_INVENTARI_REGAL)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            renderitzarObjectesRegal(data.articles);
        });
}

function renderitzarObjectesRegal(articles) {
    llistaObjectesRegal.innerHTML = '';

    articles.forEach(article => {
        const tr = document.createElement('tr');

        tr.innerHTML = `
            <td>${article.nom}</td>
            <td>${article.quantitat}</td>
            <td>
                <button class="boto-acció" onclick="confirmarRegal(${article.id})">Regalar</button>
            </td>
        `;

        llistaObjectesRegal.appendChild(tr);
    });
}

function tancarModalObjectes() {
    modalObjectes.style.display = 'none';
    modalNpcs.style.display = 'flex';
}

function confirmarRegal(idArticle) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(URL_REGALAR_ARTICLE, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({
            id_npc: npcSeleccionat,
            id_article: idArticle
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        alert(`Reacció: ${data.reaccio}`);

        modalObjectes.style.display = 'none';
        modalNpcs.style.display = 'none';
    });
}