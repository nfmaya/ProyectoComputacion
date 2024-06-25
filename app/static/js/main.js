const socket = io();

function play(choice) {
    socket.emit('play', { choice: choice });
}

socket.on('game_result', function(data) {
    document.getElementById('result').innerHTML = `You played ${data.player_choice}. Opponent played ${data.opponent_choice}. ${data.result}`;
});
