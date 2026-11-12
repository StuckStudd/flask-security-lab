from flask import Flask, request, render_template_string
import logging
import sqlite3
import time

app = Flask(__name__)

logging.basicConfig(
    filename="access.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


# --- создаём базу данных для пользователей ---
def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
    )
    conn.commit()
    conn.close()


# --- страница с формой регистрации ---
page = """
<!doctype html>
<title>Регистрация</title>
<h2>Регистрация</h2>
<form method="post" action="/register">
    <input name="username" placeholder="Логин"><br><br>
    <input name="password" placeholder="Пароль" type="password"><br><br>
    <button type="submit">Зарегистрироваться</button>
</form>
<p>Всего пользователей: {{ count }}</p>
"""


@app.before_request
def log_request():
    ip = request.remote_addr
    path = request.path
    method = request.method
    logging.info(f"{ip} {method} {path}")


@app.route("/")
def home():
    conn = sqlite3.connect("users.db")
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    return render_template_string(page, count=count)


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    # нарочно тяжёлая операция, чтобы нагрузка была заметнее
    time.sleep(0.1)

    conn = sqlite3.connect("users.db")
    conn.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
    )
    conn.commit()
    conn.close()
    return f"Пользователь {username} зарегистрирован!"


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000)