from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

app.secret_key = 'mykey'
# Авторизация
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        conn = sqlite3.connect('new.db')
        cursor = conn.cursor()
        cursor.execute('SELECT ФИО FROM Пользователи WHERE Логин=? AND Пароль=?', (login, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['user'] = user[0]
            return redirect(url_for('clients'))
        else:
            return "Неверный логин или пароль"
    return render_template('login.html')


# Страница клиентов
@app.route('/clients', methods=['GET', 'POST'])
def clients():
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('new.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Клиенты WHERE ФИО_ответственного=?', (session['user'],))
    clients = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        client_id = request.form['client_id']
        new_status = request.form['status']
        conn = sqlite3.connect('new.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE Клиенты SET Статус=? WHERE Номер_счета=?', (new_status, client_id))
        conn.commit()
        conn.close()
        return redirect(url_for('clients'))

    return render_template('clients.html', clients=clients)

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)