
const socket = io();

socket.on('game_state', (state) => {
    const gameDiv = document.getElementById('game');
    let html = `<p>Round: ${state.current_round} | Forest: ${state.forest}</p>`;
    state.players.forEach((p, i) => {
        html += `<h3>Player ${i+1}</h3>
                 <p>Woodcutters: ${p.woodcutters}</p>
                 <p>Victory Points: ${p.victory_points}</p>
                 <p>Harvested Trees: ${p.harvested_trees}</p>`;
    });
    html += `<p>Current Player: Player ${state.current_player + 1}</p>`;
    html += `
        <button onclick="act('harvest')">Harvest</button>
        <button onclick="valueAct('replant')">Replant</button>
        <button onclick="valueAct('buy_vp')">Buy VP</button>
        <button onclick="valueAct('buy_wc')">Buy WC</button>
        <button onclick="act('exchange_wc')">Exchange WC</button>
        <button onclick="act('end_turn')">End Turn</button>
    `;
    gameDiv.innerHTML = html;
});

function act(action) {
    socket.emit('action', {action});
}

function valueAct(action) {
    const val = parseInt(prompt("Enter amount:"));
    if (!isNaN(val)) {
        socket.emit('action', {action, value: val});
    }
}
