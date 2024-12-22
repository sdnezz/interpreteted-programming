from flask import Flask, request, render_template_string, jsonify
import sqlite3
import json
import os

app = Flask(__name__)

# Папка для сохранения загруженных файлов
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Подключение к базе данных и создание таблиц

def init_db():
    conn = sqlite3.connect("court_case.db")
    cursor = conn.cursor()

    # Создание таблиц
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cases (
        case_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        start_date TEXT NOT NULL,
        status TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Participants (
        participant_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL,
        case_id INTEGER NOT NULL,
        FOREIGN KEY (case_id) REFERENCES Cases(case_id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Documents (
        document_id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_title TEXT NOT NULL,
        created_date TEXT NOT NULL,
        case_id INTEGER NOT NULL,
        FOREIGN KEY (case_id) REFERENCES Cases(case_id)
    )""")

    conn.commit()
    conn.close()

# Маршрут для главной страницы
@app.route('/')
def home():
    form_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Учет судебных дел</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
                color: #333;
            }
            h1, h2 {
                color: #6a0dad;
                text-align: center;
            }
            form, a {
                display: block;
                margin: 20px auto;
                text-align: center;
                max-width: 400px;
            }
            input[type="text"], input[type="file"] {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
                box-sizing: border-box;
            }
            input[type="submit"] {
                background-color: #6a0dad;
                color: white;
                border: none;
                padding: 10px;
                cursor: pointer;
                border-radius: 5px;
            }
            input[type="submit"]:hover {
                background-color: #5c0cb2;
            }
            ul {
                list-style: none;
                padding: 0;
            }
            li {
                background: #e4e4f2;
                margin: 10px;
                padding: 10px;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <h1>Добавление судебного дела</h1>
        <form action="/add_case" method="post">
            <label for="title">Название дела:</label>
            <input type="text" id="title" name="title" placeholder="Введите название "><br><br>
            <label for="start_date">Дата начала:</label>
            <input type="text" id="start_date" name="start_date" placeholder="YYYY-MM-DD"><br><br>
            <label for="status">Статус:</label>
            <input type="text" id="status" name="status" placeholder="Статус дела"><br><br>
            <input type="submit" value="Добавить дело">
        </form>

        <h2>Посмотреть данные</h2>
        <a href="/view_cases">Посмотреть дела</a><br><br>

        <h2>Экспорт/Импорт JSON</h2>
        <a href="/export_json">Экспортировать в JSON</a><br>
        <form action="/import_json" method="post" enctype="multipart/form-data">
            <label for="json_file">Загрузка JSON-файла:</label>
            <input type="file" id="json_file" name="json_file"><br><br>
            <input type="submit" value="Импортировать">
        </form>
    </body>
    </html>
    """
    return render_template_string(form_html)

# Прочие маршруты...

# Маршрут для добавления дела
@app.route('/add_case', methods=['POST'])
def add_case():
    title = request.form['title']
    start_date = request.form['start_date']
    status = request.form['status']

    conn = sqlite3.connect("court_case.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Cases (title, start_date, status) VALUES (?, ?, ?)", (title, start_date, status))
    conn.commit()
    conn.close()

    return "Дело успешно добавлено! <a href='/'>Вернуться назад</a>"

# Маршрут для просмотра дел
@app.route('/view_cases')
def view_cases():
    conn = sqlite3.connect("court_case.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cases")
    cases = cursor.fetchall()
    conn.close()

    cases_html = "<h1>Список дел</h1><ul>"
    for case in cases:
        cases_html += f"<li>ID: {case[0]}, Название: {case[1]}, Дата начала: {case[2]}, Статус: {case[3]}</li>"
    cases_html += "</ul><a href='/'>Вернуться назад</a>"
    return cases_html

# Экспорт данных в JSON
@app.route('/export_json')
def export_json():
    conn = sqlite3.connect("court_case.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cases")
    cases = cursor.fetchall()
    conn.close()

    with open("cases.json", "w") as file:
        json.dump(cases, file)

    return "Данные экспортированы в файл cases.json! <a href='/'>Вернуться назад</a>"

# Импорт данных из JSON
@app.route('/import_json', methods=['POST'])
def import_json():
    if 'json_file' not in request.files:
        return "Файл не найден! <a href='/'>Вернуться назад</a>"

    file = request.files['json_file']
    if file.filename == '':
        return "Файл не выбран! <a href='/'>Вернуться назад</a>"

    if file and file.filename.endswith('.json'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        with open(file_path, 'r') as f:
            cases = json.load(f)

        conn = sqlite3.connect("court_case.db")
        cursor = conn.cursor()
        cursor.executemany("""
        INSERT INTO Cases (title, start_date, status) 
        VALUES (:title, :start_date, :status)
        """, cases)

        conn.commit()
        conn.close()

        return "Данные успешно импортированы из JSON! <a href='/'>Вернуться назад</a>"

    return "Неверный формат файла! Пожалуйста, выберите файл .json. <a href='/'>Вернуться назад</a>"

# Инициализация БД при запуске
if __name__ == '__main__':
    init_db()
    app.run(debug=True)