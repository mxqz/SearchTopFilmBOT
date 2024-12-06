from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_mysqldb import MySQL
import bcrypt
import binascii
import logging

app = Flask(__name__)

# Конфігурація MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Ваш користувач MySQL
app.config['MYSQL_PASSWORD'] = 'rO8cD%k3$z'  # Ваш пароль MySQL
app.config['MYSQL_DB'] = 'SearchTopFilmBot'  # Назва вашої бази даних

# Ініціалізація MySQL
mysql = MySQL(app)

# Хешування паролів
def hash_password(password):
    # Генерація salt та хешування пароля
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Перетворення хешу в hex формат (стрічка, яку можна зберігати)
    return binascii.hexlify(hashed_password).decode('utf-8')

# Функція для перевірки пароля
def check_password(password, hashed_password):
    # Відновлення хешу з hex-формату
    hashed_password_bytes = binascii.unhexlify(hashed_password.encode('utf-8'))
    # Перевірка введеного пароля
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password_bytes)

# Список фільмів (для тесту)
FILMS = [
    {"id": 1, "name": "Inception"},
    {"id": 2, "name": "Interstellar"},
    {"id": 3, "name": "The Matrix"}
]

# Маршрут для головної сторінки
@app.route('/')
def home():
    return render_template('index.html', active_tab='films', search_results=None, error=None)

# Маршрут для пошуку
@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    tab = request.args.get('tab', 'films')  # Отримуємо вибрану вкладку
    error = None
    results = []

    try:
        # Підключення до бази даних через Flask-MySQLdb
        cursor = mysql.connection.cursor()

        # Виконання SQL-запиту залежно від активної вкладки
        if tab == 'films':
            cursor.execute("SELECT * FROM films WHERE title LIKE %s", (f"%{query}%",))
        elif tab == 'series':
            cursor.execute("SELECT * FROM series WHERE title LIKE %s", (f"%{query}%",))
        elif tab == 'anime':
            cursor.execute("SELECT * FROM anime WHERE title LIKE %s", (f"%{query}%",))
        elif tab == 'manga':
            cursor.execute("SELECT * FROM manga WHERE title LIKE %s", (f"%{query}%",))
        else:
            error = "Невідома вкладка."

        # Отримання результатів
        if not error:
            results = cursor.fetchall()

    except Exception as e:
        error = "Немає доступу до бази даних. Перевірте підключення."
        print(f"Database error: {e}")  # Лог помилки у консолі для дебагу
    finally:
        # Закриття курсора
        cursor.close()

    # Повертаємо HTML з результатами або повідомленням про помилку
    return render_template(
        'index.html',
        active_tab=tab,
        search_results=results,
        error=error
    )

# Маршрут для реєстрації
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    hashed_password = hash_password(password)
    
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO user_database (username, password_hash) VALUES (%s, %s)', (username, hashed_password))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'success': True})

# Маршрут для авторизації
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT password_hash FROM user_database WHERE username = %s', (username,))
    result = cursor.fetchone()
    
    if result and check_password(password, result[0]):
        # Повертаємо успішну відповідь і ім'я користувача
        return jsonify({'success': True, 'username': username})
    else:
        return jsonify({'success': False, 'message': 'Невірні дані для входу'})
    
@app.route('/logout', methods=['POST'])
def logout():
    # Логіка виходу, наприклад, очищення сесії
    session.pop('user', None)  # Якщо ви використовуєте сесії для збереження даних про користувача

    return jsonify({'success': True})



logging.basicConfig(level=logging.DEBUG)

@app.errorhandler(404)
def page_not_found(e):
    return "Сторінку не знайдено!", 404

if __name__ == '__main__':
    app.run(debug=True)
