import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class NimGame:
    def __init__(self, piles, current_player):
        self.piles = piles
        self.current_player = current_player

    def is_game_over(self):
        return sum(self.piles) == 0

    def make_move(self, pile_index, remove_count):
        if 0 <= pile_index < len(self.piles) and 1 <= remove_count <= self.piles[pile_index]:
            self.piles[pile_index] -= remove_count
            if not self.is_game_over():
                self.current_player = "Computer" if self.current_player == "Player" else "Player"

    def to_dict(self):
        return {"piles": self.piles, "current_player": self.current_player}

def load_game_data():
    try:
        with open('game_data.json', 'r') as file:
            data = json.load(file)
            return NimGame(data['piles'], data['current_player'])
    except FileNotFoundError:
        return NimGame([3, 4, 5], "Player")

def save_game_data(game):
    with open('game_data.json', 'w') as file:
        json.dump(game.to_dict(), file)

game = load_game_data()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pile_index = int(request.form['pile_index'])
        remove_count = int(request.form['remove_count'])
        game.make_move(pile_index, remove_count)
        save_game_data(game)
        if game.is_game_over():
            return redirect(url_for('game_over'))

    return render_template('index.html', game=game)

@app.route('/game_over')
def game_over():
    winner = "Player" if game.current_player == "Computer" else "Computer"
    return render_template('game_over.html', winner=winner)

if __name__ == '__main__':
    app.run(debug=True)
