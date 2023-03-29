from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommendations', methods=['POST'])
def recommendations():
    # Get the user's preferences from the form
    input_type = request.form['input_type']
    steam_id = None
    game_list = None
    if input_type == 'steam_id':
        steam_id = request.form['steam_id']
    elif input_type == 'game_list':
        game_list = request.form['game_list'].split(',')

    # Call our recommendation system function with the user's preferences and get the recommended games
    games = ['Game 1', 'Game 2', 'Game 3']  # Just an example input for display purposes. Try running with app.run().

    # Render a template with the recommended games
    return render_template('recommendations.html', games=games)


if __name__ == '__main__':
    app.run()
