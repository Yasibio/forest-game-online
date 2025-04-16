
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from game_logic import GameModel

app = Flask(__name__)
socketio = SocketIO(app)

game = GameModel()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    emit('game_state', game.get_state())

@socketio.on('action')
def on_action(data):
    action = data.get('action')
    value = data.get('value', 0)
    if game.game_over:
        emit('game_state', game.get_state(), broadcast=True)
        return

    if action == "harvest":
        game.harvest()
    elif action == "replant":
        game.replant(value)
    elif action == "buy_vp":
        game.buy_vp(value)
    elif action == "buy_wc":
        game.buy_wc(value)
    elif action == "exchange_wc":
        game.exchange_wc()
    elif action == "end_turn":
        game.end_turn()

    emit('game_state', game.get_state(), broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
