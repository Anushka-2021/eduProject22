from flask import Flask, request, render_template, session
import requests, base64, sqlite3, datetime

app = Flask(__name__)

conn = sqlite3.connect("edubd.db")
cursor = conn.cursor()

host = 'judge0-ce.p.rapidapi.com'
sent_adress = 'https://' + host + '/submissions/'
tok_n = '1806363f0fmshf3926631702e101p1eda9ajsn5e10975d9be7'

heads = {
    'Content-type': 'application/json',
    'X-RapidAPI-Key':tok_n,
    'X-RapidApi-Host': host
}
langes = [{'id': 52, 'name': 'C++ (GCC 7.4.0)'}, {'id': 54, 'name': 'C++ (GCC 9.2.0)'}, {'id': 62, 'name': 'Java (OpenJDK 13.0.1)'}, {'id': 71, 'name': 'Python (3.8.1)'}]
app.secret_key = '1806363f0fmshf3926631702e101p1eda9ajsn5e10975d9be7'

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template("login.html")


if __name__ == '__main__':
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_table_1
    (user_id UNIQUE, username, mail, password, role)
    """)
    conn.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS tasks
    (task_id UNIQUE, task_text, author, tests, exp_output)
    """)
    conn.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS solutions
    (sol_id UNIQUE, lang, code, input, time_of_sol, day_of_sol)
    """)
    conn.commit()

    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
