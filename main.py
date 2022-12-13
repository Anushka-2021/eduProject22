from flask import Flask, request, render_template, session
import requests, base64, sqlite3, datetime

app = Flask(__name__)

conn = sqlite3.connect("edubd.db")
cursor = conn.cursor()

host = 'judge0-ce.p.rapidapi.com'
#sent_adress = 'https://' + host + '/submissions/'
sent_adress = 'https://judge0-ce.p.rapidapi.com/submissions/'
tok_n = '1806363f0fmshf3926631702e101p1eda9ajsn5e10975d9be7'
tok_n1 = 'd42fc9aa74msh76c0f87fb2e4c69p154805jsn22c7d1cbb6b2'
tok_n2 = '3c5493c344mshc227e55d5d22af6p165d18jsn83a124652256'

heads = {
    'Content-Type': 'application/json',
    'X-RapidAPI-Key':tok_n1,
    'X-RapidApi-Host': host
}
langes = [{'id': 52, 'name': 'C++ (GCC 7.4.0)'}, {'id': 54, 'name': 'C++ (GCC 9.2.0)'}, {'id': 62, 'name': 'Java (OpenJDK 13.0.1)'}, {'id': 71, 'name': 'Python (3.8.1)'}]
app.secret_key = '1806363f0fmshf3926631702e101p1eda9ajsn5e10975d9be7'

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template("login.html")

#@app.route('/', methods = ['GET', 'POST'])
#def ap():
#    return render_template("task1.html")

@app.route('/', methods = ['GET', 'POST'])
def task():
    if request.method == 'POST':
        Code = base64.b64encode(request.form.get('code_area').encode("UTF-8")).decode("UTF-8")
        myCodeLanguage = request.form.get('language')
        #myCin = request.form.get('cin')
        M = base64.b64encode(request.form.get('cin').encode("UTF-8")).decode("UTF-8")
        dats = {
            "language_id": myCodeLanguage,
            "source_code": Code,
            "stdin": M,
            "expected_output": M
        }
        resp = requests.request("POST", sent_adress, headers = heads, json = dats, params = {"base64_encoded": "true"}).json()
        #response = requests.request("POST", sent_adress, headers = heads, json = dats, params = {"base64_encoded": "true"})

        if resp['token'] is not None:
            decision_tok_n = resp['token']
            answer = requests.request("GET", sent_adress + decision_tok_n, headers = heads, params = {"base64_encoded": "true"}).json()
        else:
            return render_template("task1.html", data = "Mistake", langs = langes)

        data = answer['stdout']

        #decoding output
        output = base64.b64decode(data.encode("UTF-8")).decode("UTF-8")

        return render_template('task1.html', rets = output, res = answer['status']['description'], langs = langes)

    return render_template("task1.html", langs = langes)


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


