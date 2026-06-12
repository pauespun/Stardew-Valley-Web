const btnPescarPort = document.getElementById('btn-pescar-port');
const modalMinijoc = document.getElementById('modal-minijoc');
const modalResultat = document.getElementById('modal-resultat-pesca');
const btnMantenir = document.getElementById('btn-mantenir-pescar');
const barraProgres = document.getElementById('barra-progres-pesca');
const textPeix = document.getElementById('nom-peix-capturat');
const textQualitat = document.getElementById('qualitat-peix-capturat');

let progres = 0;
let intervalPesca = null;
let pescant = false;

const llistaPeixos = ["Llobarro", "Carpa", "Sardina", "Tonyina", "Poma", "Bota Vella"];
const llistaQualitats = ["Normal", "Plata", "Or"];

btnPescarPort.addEventListener('click', obrirMinijoc);

btnMantenir.addEventListener('mousedown', iniciarPujada);
btnMantenir.addEventListener('mouseup', aturarPujada);
btnMantenir.addEventListener('mouseleave', aturarPujada);

function obrirMinijoc() {
    progres = 0;
    barraProgres.style.width = '0%';
    modalMinijoc.style.display = 'flex';
}

function tancarMinijoc() {
    aturarPujada();
    modalMinijoc.style.display = 'none';
}

function iniciarPujada() {
    if (pescant) return;
    pescant = true;
    
    intervalPesca = setInterval(() => {
        progres += 1.5;
        if (progres >= 100) {
            progres = 100;
            barraProgres.style.width = '100%';
            aturarPujada();
            finalitzarPesca();
        } else {
            barraProgres.style.width = progres + '%';
        }
    }, 30);
}

function aturarPujada() {
    pescant = false;
    if (intervalPesca) {
        clearInterval(intervalPesca);
        intervalPesca = null;
    }
}

function finalitzarPesca() {
    modalMinijoc.style.display = 'none';
    
    const peixAleatori = llistaPeixos[Math.floor(Math.random() * llistaPeixos.length)];
    const qualitatAleatoria = llistaQualitats[Math.floor(Math.random() * llistaQualitats.length)];
    
    textPeix.innerText = peixAleatori;
    
    if (peixAleatori === "Bota Vella" || peixAleatori === "Poma") {
        textQualitat.innerText = "Deixalles";
        textQualitat.style.borderColor = "#9e9e9e";
        textQualitat.style.backgroundColor = "#e0e0e0";
    } else {
        textQualitat.innerText = `Qualitat: ${qualitatAleatoria}`;
        if (qualitatAleatoria === "Or") {
            textQualitat.style.borderColor = "#ff8f00";
            textQualitat.style.backgroundColor = "#fff8e1";
        } else if (qualitatAleatoria === "Plata") {
            textQualitat.style.borderColor = "#757575";
            textQualitat.style.backgroundColor = "#f5f5f5";
        } else {
            textQualitat.style.borderColor = "#4e342e";
            textQualitat.style.backgroundColor = "#d7ccc8";
        }
    }
    
    modalResultat.style.display = 'flex';
}

function agafarPeix() {
    modalResultat.style.display = 'none';
}

function tirarPeix() {
    modalResultat.style.display = 'none';
}
