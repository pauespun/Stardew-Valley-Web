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

// NOUS ELEMENTS DEL MODAL DE REACCIÓ
const modalReaccio = document.getElementById('modal-reaccio');
const textReaccio = document.getElementById('text-reaccio');

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
                🎂 ${npc.aniversari}<br>
                ❤️ ${npc.amistat}/10
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
        // En lloc d'alert(), utilitzem la nova finestra
        if (data.error) {
            textReaccio.innerHTML = `<strong>Error:</strong><br>${data.error}`;
            modalObjectes.style.display = 'none';
            modalReaccio.style.display = 'flex';
            return;
        }

        // Afegim una mica de sabor (emojis) segons la reacció
        let icona = "😐";
        let reaccioNeta = data.reaccio;
        
        if (reaccioNeta.includes("M'encanta")) icona = "🥰";
        else if (reaccioNeta.includes("M'agrada")) icona = "😊";
        else if (reaccioNeta.includes("odio")) icona = "🤢";

        textReaccio.innerHTML = `<strong>${reaccioNeta}</strong> ${icona}`;

        // Amaguem els altres modals i mostrem el de la reacció
        modalObjectes.style.display = 'none';
        modalNpcs.style.display = 'none';
        modalReaccio.style.display = 'flex';
    });
}

// NOU: Funció per tancar el modal de reacció
function tancarModalReaccio() {
    modalReaccio.style.display = 'none';
    
    // Tornem a obrir la llista de NPCs perquè el jugador pugui veure com ha pujat el seu cor ❤️
    obrirModalNpcs();
}
