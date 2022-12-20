from flask import Flask, request, render_template, session
import requests, base64, sqlite3, datetime

app = Flask(__name__)

conn = sqlite3.connect("edubd.db", check_same_thread=False)
cursor = conn.cursor()

host = 'judge0-ce.p.rapidapi.com'
#sent_adress = 'https://' + host + '/submissions/'
sent_adress = 'https://judge0-ce.p.rapidapi.com/submissions/'
multi_sent_adress = 'https://judge0-ce.p.rapidapi.com/submissions/batch'
tok_n = '1806363f0fmshf3926631702e101p1eda9ajsn5e10975d9be7'
tok_n1 = 'd42fc9aa74msh76c0f87fb2e4c69p154805jsn22c7d1cbb6b2'
tok_n2 = '3c5493c344mshc227e55d5d22af6p165d18jsn83a124652256'
tok_n3 = 'eafe8c11d6msh034ae0f1f65da8fp173280jsn6a1a229e0da5'
tok_n4 = '0162c9aafemsh8679d6259f6332ap18330djsn2150317c1201'

heads = {
    'Content-Type': 'application/json',
    'X-RapidAPI-Key':tok_n3,
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
        if myCodeLanguage is None:
            return render_template("compiller.html", data="Please choose language", langs = langes)

        myCin = base64.b64encode(request.form.get('cin').encode("UTF-8")).decode("UTF-8")
        dats = {
            "language_id": myCodeLanguage,
            "source_code": Code,
            "stdin": myCin,
            "expected_output": myCin
        }
        resp = requests.request("POST", sent_adress, headers = heads, json = dats, params = {"base64_encoded": "true"}).json()
        #response = requests.request("POST", sent_adress, headers = heads, json = dats, params = {"base64_encoded": "true"})

        if resp['token'] is not None:
            decision_tok_n = resp['token']
            answer = requests.request("GET", sent_adress + decision_tok_n, headers = heads, params = {"base64_encoded": "true"}).json()
        else:
            return render_template("compiller.html", data = "Mistake", langs = langes)

        data = answer['stdout']


        #decoding output
        if data == None:
            return render_template('compiller.html', rets = data, res = answer['status']['description'], langs = langes)
        output = base64.b64decode(data.encode("UTF-8")).decode("UTF-8")


        return render_template('compiller.html', rets = output, res = answer['status']['description'], langs = langes)

    return render_template("compiller.html", langs = langes)

@app.route('/task1', methods = ['GET', 'POST'])
def send_task():
    if request.method == 'POST':
        #as / start
        Code = base64.b64encode(request.form.get('code_area').encode("UTF-8")).decode("UTF-8")
        myCodeLanguage = request.form.get('language')
        if myCodeLanguage is None:
            return render_template("task1.html", data="Please choose language", langs = langes)

        #myCin = base64.b64encode(request.form.get('cin').encode("UTF-8")).decode("UTF-8")

        #testing
        cursor.execute("SELECT tests FROM tasks WHERE task_id=?", ('1', ))
        q = cursor.fetchall()[0][0]

        noun = 0
        testCin = ''
        testCout = ''
        w = q.split()
        subs = []
        st = ''
        flag = 0
        for i in q:
            if i == ';':
                noun +=1

                #adding ane of subs in a row
                if testCin != '':
                    testCin = base64.b64encode(testCin.encode("UTF-8")).decode("UTF-8")
                    testCout = base64.b64encode(testCout.encode("UTF-8")).decode("UTF-8")
                    f = {"language_id": myCodeLanguage,
                         "source_code": Code,
                         "stdin": testCin,
                         "expected_output": testCout}
                    subs.append(f)
                #print(subs)

                #nulling
                testCin = ''
                testCout = ''
                flag = 0
            elif i == '=':
                flag = 1
            else:
                if flag == 1:
                    testCout += i + ' '
                else:
                    testCin += i + ' '

        print(subs)
        spending_pack = {"submissions": subs}
        respos = requests.request("POST", multi_sent_adress, params = {"base64_encoded": "true"}, json = spending_pack, headers = heads).json()
        tokens = ''
        #respos = [{'token': '0e612122-2e01-494c-aa7e-0b5072dbd764'}, {'token': '8d5fb1e1-f482-4228-8389-07e575150ffa'}, {'token': 'ff126b81-c013-40f8-9dde-79db93a80945'}]
        print(respos)

        # datetime = day, time
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        day = now.strftime("%d/%m/%y")

        if respos[0]['token']:
            for i in respos:
                tokens += i['token'] + ','

                # sol_id = i
            i = 0
            cursor.execute("SELECT * FROM solutions2")
            f = cursor.fetchone()
            while f:
                i += 1
                f = cursor.fetchone()
            solution_id = i + 1

            cursor.execute("INSERT OR REPLACE INTO solutions2(sol_id, task_id, lang, code, percents, time_of_sol, day_of_sol) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (solution_id, 1, myCodeLanguage, Code, 0, time, day))
            conn.commit()

            #zapros resultatov resheniya
            answer = requests.request("GET", multi_sent_adress, headers = heads, params = {"base64_encoded": "true", "tokens": tokens, "fields": "*"}).json()
            for i in answer['submissions']:
                print(i['status'])
                if i['status']['id'] == 1 or i['status']['id'] == 2:
                    for i in range(100):
                        i += 1
                elif i['status']['id'] != 3:
                    return render_template("task1.html", rets = i['status']['description'], langs = langes)
            return render_template("task1.html", rets = "Success!", langs = langes)

        return render_template("task1.html", data="Mistakeeee", langs = langes)


        return render_template("task1.html", data="Please choose language", langs = langes)
        resp = requests.request("POST", sent_adress, headers = heads, json = dats, params = {"base64_encoded": "true"})
        #response = requests.request("POST", sent_adress, headers = heads, json = dats, params = {"base64_encoded": "true"})
        print(resp.json())
        print(heads)
        if resp == "Response [429]":
            print("OOps")
            #return render_template("task1.html", data = "Mistake", langs = langes)
        elif resp == "Response [200]":# or "Response [201]":
            resp = resp.json()
            decision_tok_n = resp['token']
            answer = requests.request("GET", sent_adress + decision_tok_n, headers = heads, params = {"base64_encoded": "true"}).json()
        else:
            return render_template("task1.html", data = "Mistake", langs = langes)

        data = answer['stdout']
        st_tus = answer['status']['description']

        #decoding output
        output = base64.b64decode(data.encode("UTF-8")).decode("UTF-8")
        #as / finished


        #testing
        cursor.execute("SELECT tests FROM tasks WHERE task_id=?", ('1', ))
        q = cursor.fetchall()[0][0]
        print(q)

        testCin = ''
        testCout = ''
        w = q.split()
        print(w)
        subs = {}
        st = ''
        marker = 1
        for i in q:
            if i != ';':
                if i == '=':
                    print(i, 'i==')
                    marker = 0
                elif i != '=':
                    print(i, ' i!=')
                    if marker == 0:
                        testCout += i + ' '
                        marker = 1
                        print(testCout + '?')
                        print(marker)
                    elif marker == 1:
                        testCin += i + ' '
                        marker = 0
            else:
                print(testCin)
                print(testCout)
                testCin = ''
                testCout = ''

        #respos = requests.request("POST", sent_adress, headers = heads, json = dats, params = {"base64_encoded": "true"})

        dats = {
            "language_id": myCodeLanguage,
            "source_code": Code,
            "stdin": testCin,
            "expected_output": testCout
        }
        #end of testing

        #cursor.execute("SELECT OR REPLACE INTO solutions2(sol_id, task_id, lang, code, input, status, percents, time_of_sol, day_of_sol)",
        #               (solution_id, 1, myCodeLanguage, Code, myCin, st_tus, 0, time, day))
        #conn.commit()


        return render_template('task1.html', rets = output, res = st_tus, langs = langes)

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

    cursor.execute("""CREATE TABLE IF NOT EXISTS solutions2
    (sol_id UNIQUE, task_id, lang, code, input, status, percents, time_of_sol, day_of_sol)
    """)
    conn.commit()

    #adding task1 handly
    #tests format: json - [{"left": a1, "right": b1, "result": c1}, {"left": a2, "right": b2, "result": c2},]
    #tests format current: json - [{"input1": string, "output1": str}, {"input2": str, "output2": str}]
    task1_text = "Задача №1: Саша решил посчитать сколько у него яблок в двух рауках. Помогите ему сделать это, написав программу на одном из предложенных языков. На вход подаётся два числа: число яблок в правой и левой руках соответственно. Входные данные: два целых числа Выходные данные: одно целое число - количество яблок. Примечание: используйте ввод и вывод с клавиатуры"
    #inp = [{"left":1, "right":1, "result":2}, {"left":3, "right":1, "result":4}, {"left":4, "right":-3, "result":1}]
    inp = [{"input": '1 1', "output": '2'}, {"input": '3 1', "output": '4'}, {"input": '4 -3', "output": '1'}]
    str = ''
    a = 0
    for i in inp:
        str+=inp[a]['input'] + ' = ' + inp[a]['output'] + ' ; '
        a += 1

    #cursor.execute("SELECT * FROM tasks")
    #f = cursor.fetchall()

    cursor.execute("INSERT OR REPLACE INTO tasks(task_id, task_text, tests) VALUES (?, ?, ?)", ("1", task1_text, str))
    conn.commit()
    #finiahed adiing tests

    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/