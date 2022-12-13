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