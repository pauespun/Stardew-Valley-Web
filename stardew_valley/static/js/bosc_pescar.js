const btnPescarBosc = document.getElementById('btn-pescar-bosc');
const modalMinijoc = document.getElementById('modal-minijoc');
const modalResultat = document.getElementById('modal-resultat-pesca');
const btnMantenir = document.getElementById('btn-mantenir-pescar');
const barraProgres = document.getElementById('barra-progres-pesca');
const textPeix = document.getElementById('nom-peix-capturat');
const textQualitat = document.getElementById('qualitat-peix-capturat');

let progres = 0;
let intervalPesca = null;
let pescant = false;

const llistaPeixos = ["Perca", "Rútil", "Lluç de riu", "Silur petit", "Branca", "Sabatilla vella"];
const llistaQualitats = ["Normal", "Plata", "Or"];

btnPescarBosc.addEventListener('click', obrirMinijoc);

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

    fetch(URL_GENERAR_PEIX)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            textPeix.innerText = data.nom;
            textQualitat.innerText = `Qualitat: ${data.qualitat}`;

            modalResultat.style.display = 'flex';
        });
}

function agafarPeix() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(URL_AGAFAR_PEIX, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        modalResultat.style.display = 'none';

        const energia = document.getElementById("energia");
        if (energia) {
            energia.innerText = data.energia;
        }
    });
}

function tirarPeix() {
    modalResultat.style.display = 'none';
}
