const seccionBatalla = document.getElementById('campo-batalla');
const msjBatalla = document.getElementById('msj-batalla');
const imgAtaqueJugador = document.getElementById('img-ataque-jugador');
const imgAtaquePc = document.getElementById('img-ataque-pc');
const btnPiedra = document.getElementById('btn-piedra');
const btnPapel = document.getElementById('btn-papel');
const btnTijeras = document.getElementById('btn-tijeras');
const btnContinuar = document.getElementById('btn-continuar');

let opcionJugador;
let opcionPc;
let imgJugador;
let imgPc;

var socket = io();
var choice = null;
var room = "{{ room_id }}";



const imagenes = [
    {
        name: "Piedra",
        url: "../assets/Piedra.PNG" 
    },
    {
        name: "Papel",
        url: "../assets/Papel.PNG" 
    },
    {
        name: "Tijeras",
        url: "../assets/Tijeras.PNG" 
    }
];

btnPiedra.addEventListener('click', function() {
    choose('rock');
});

btnPapel.addEventListener('click', function() {
    choose('paper');
});


btnTijeras.addEventListener('click', function() {
    choose('scissors');
});

btnContinuar.addEventListener('click', function() {
    continuePlay();
});


function choose(selectedChoice) {
    choice = selectedChoice;
    document.getElementById('result').innerText = `Elegiste ${choice}. Click continuar para jugar.`;
}

function continuePlay() {
    if (choice) {
       return socket.emit('play', { room: room, choice: choice });
    } else {
        return alert('Debe elegir una opcion antes de seguir.');
    }
}

socket.on('game_result', function(data) {
    document.getElementById('result').innerText = `You played ${data.player1_choice}. Opponent played ${data.player2_choice}. Result: ${data.result}`;
});

socket.on('error', function(data) {
    alert(data.error);
});

socket.on('waiting', function(data) {
    document.getElementById('result').innerText = data.message;
});

socket.on('room_created', function(data) {
    room = data.room_id;
    document.getElementById('result').innerText = 'Room created. Waiting for another player to join.';
});

socket.on('room_joined', function(data) {
    room = data.room_id;
    document.getElementById('result').innerText = 'Room joined. Make your choice.';
});


document.addEventListener("DOMContentLoaded", () => {
    const socket = io();

    document.querySelectorAll(".btn-ataques").forEach(img => {
        img.addEventListener("click", () => {
            //const choice = img.id.replace("btn-", ""); 
            
            console.log("Eleccion:"+choice);

            socket.emit("play", { choice });
        });
    });

    socket.on("game_update", data => {
        document.getElementById("player1_choice").innerText = data.player1_choice || "Waiting for Player 1";
        document.getElementById("player2_choice").innerText = data.player2_choice || "Waiting for Player 2";
        if (data.winner !== null) {
            document.getElementById("winner").innerText = `Winner: Player ${data.winner}`;
        }
    });
});