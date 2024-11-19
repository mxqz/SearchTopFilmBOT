from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Список фільмів (для тесту)
FILMS = [
    {"id": 1, "name": "Inception"},
    {"id": 2, "name": "Interstellar"},
    {"id": 3, "name": "The Matrix"}
]

# Маршрут для головної сторінки
@app.route('/')
def home():
    return render_template('index.html')

# Маршрут для пошуку фільмів
@app.route('/api/search')
def search():
    query = request.args.get('q', '').lower()
    results = [film for film in FILMS if query in film['name'].lower()]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
