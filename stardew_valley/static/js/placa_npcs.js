const nomsStardew = ["Abigail", "Alex", "Caroline", "Clint", "Demetrius", "Elliott", "Emily", "Evelyn", "George", "Gus", "Haley", "Harvey", "Jas", "Jodi", "Kent", "Krobus", "Leah", "Lewis", "Linus", "Marnie", "Maru", "Pam", "Penny", "Pierre", "Robin", "Sam", "Sandy", "Sebastian", "Shane", "Willy"];
const npcs = [];

for (let i = 0; i < 30; i++) {
    npcs.push({
        nom: nomsStardew[i],
        aniversari: `${Math.floor(Math.random() * 28) + 1} Primavera`,
        relacio: Math.floor(Math.random() * 11)
    });
}

let paginaActual = 1;
const itemsPerPagina = 6;

const modalNpcs = document.getElementById('modal-npcs');
const modalObjectes = document.getElementById('modal-objectes');
const llistaNpcs = document.getElementById('llista-npcs');
const textPaginacio = document.getElementById('text-paginacio');
const btnRegalarPrincipal = document.getElementById('btn-regalar-principal');
const btnPrev = document.getElementById('btn-prev');
const btnNext = document.getElementById('btn-next');
const titolModalObjectes = document.getElementById('titol-modal-objectes');

btnRegalarPrincipal.addEventListener('click', obrirModalNpcs);
btnPrev.addEventListener('click', () => canviarPagina(-1));
btnNext.addEventListener('click', () => canviarPagina(1));

function obrirModalNpcs() {
    modalNpcs.style.display = 'flex';
    renderitzarNpcs();
}

function tancarModalNpcs() {
    modalNpcs.style.display = 'none';
}

function renderitzarNpcs() {
    llistaNpcs.innerHTML = '';
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
                ❤️ ${npc.relacio}/10
            </div>
            <button class="boto-acció" onclick="obrirModalObjectes('${npc.nom}')">Regalar</button>
        `;
        llistaNpcs.appendChild(targeta);
    });

    textPaginacio.innerText = `Pàgina ${paginaActual} / 5`;
}

function canviarPagina(direccio) {
    paginaActual += direccio;
    if (paginaActual < 1) paginaActual = 1;
    if (paginaActual > 5) paginaActual = 5;
    renderitzarNpcs();
}

function obrirModalObjectes(nomNpc) {
    titolModalObjectes.innerText = `Regalar a ${nomNpc}`;
    modalNpcs.style.display = 'none';
    modalObjectes.style.display = 'flex';
}

function tancarModalObjectes() {
    modalObjectes.style.display = 'none';
    modalNpcs.style.display = 'flex';
}

function confirmarRegal() {
    modalObjectes.style.display = 'none';
    modalNpcs.style.display = 'none';
}
