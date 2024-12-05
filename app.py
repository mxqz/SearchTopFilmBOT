###Todo list###
#написати БД
#підключити БД
#тестування багів
#доробити дизайн для пошуку та помилок

from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

#Налаштування підключення до бази даних
db_config = {                                                     #<--- зробити підчас підключення БД
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'your_database_name'
}
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

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    tab = request.args.get('tab', 'films')  # Отримуємо вибрану вкладку
    error = None
    results = []

    try:
        # Спроба підключення до бази даних
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

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

    except Error as e:
        error = "Немає доступу до бази даних. Перевірте підключення."
        print(f"Database error: {e}")  # Лог помилки у консолі для дебагу
    except Exception as e:
        error = "Сталася несподівана помилка."
        print(f"General error: {e}")  # Лог інших помилок у консолі
    finally:
        # Закриття підключення до бази даних, якщо воно було відкрито
        if 'connection' in locals() and connection.is_connected():
            connection.close()

    # Повертаємо HTML з результатами або повідомленням про помилку
    return render_template(
        'index.html',
        active_tab=tab,
        search_results=results,
        error=error
    )

if __name__ == '__main__':
    app.run(debug=True)

# Головна сторінка з пошуковою формою
# @app.route('/')
# def index():                                                                      <--- попередня версія пошуку
#     return '''
#         <form action="/search" method="get">
#             <input type="text" name="query" placeholder="Введіть запит для пошуку" required>
#             <button type="submit">Пошук</button>
#         </form>
#     '''


# Обробник пошукового запиту

