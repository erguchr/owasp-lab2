import sqlite3
from flask import *
from database import path

app = Flask(__name__)
app.secret_key = "jsvjvwrbjvwhfhiuhrvh"

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name = request.form['username']
        pas = request.form['password']

        con = sqlite3.connect(path)
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO users (username, password)"
                        "VALUES (?, ?)", (name, pas))
            con.commit()
            return redirect('/login')
        except sqlite3.IntegrityError:
            return render_template('register.html', error="Такой логин уже занят")
        finally:
            con.close()

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        pas = request.form['password']

        con = sqlite3.connect(path)
        cur = con.cursor()

        cur.execute('SELECT id FROM users WHERE username = ? AND password = ?', (name, pas))
        user = cur.fetchone()
        con.close()
        if user is not None:
            session['user_id'] = user[0]
            return redirect('/')
        else:
            return render_template('login.html', error="Неверный логин или пароль")
    return render_template('login.html')

@app.route('/', methods = ['GET','POST'])
def mainpage():
    if 'user_id' not in session :
        return redirect('/login')

    con = sqlite3.connect(path)
    cur = con.cursor()

    if request.method == 'POST':
        task = request.form['content']

        cur.execute('INSERT INTO tasks (user_id, content) VALUES (?, ?)',(session['user_id'], task))

        con.commit()
        con.close()

        return redirect('/')
    else:
        cur.execute('SELECT id, content FROM tasks WHERE user_id = ?',(session['user_id'],))
        all_tasks = cur.fetchall()
        con.close()
        return render_template('index.html', tasks = all_tasks)

@app.route('/logout', methods = ['GET'])
def logout():
    session.pop('user_id', None)
    return redirect('/login')

@app.route('/delete/<int:task_id>', methods = ['POST'])
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect('/login')

    con = sqlite3.connect(path)
    cur = con.cursor()

    cur.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

    con.commit()
    con.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)