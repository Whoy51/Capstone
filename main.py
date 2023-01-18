from flask import Flask, render_template, request, redirect, url_for
import time
import sqlite3

app = Flask(__name__)

con = sqlite3.connect("data.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(name, studentid,  teacher)")


# cur.executemany("""INSERT INTO person VALUES (?, ?)""", [(name, age)])
# res = cur.execute("SELECT name FROM person")

def post():
    print("post")


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['studentid'] == 'admin' or request.form['password'] == 'admin':
            return redirect(url_for('admin'))
        elif request.form['studentid'] == 'test' and request.form['password'] == 'test':
            return redirect(url_for('student'))
        else:
            error = "Invalid Credentials"
    return render_template('index.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        studentid = request.form['studentid']
        teachers = request.form['teachers']

        if teachers == "Unselected" or len(name) == 0 or len(studentid) == 0:
            s = " "
            if len(name) == 0:
                s += "name "
            if len(studentid) == 0:
                s += "studentid "
            if teachers == "Unselected":
                s += "teachers "
            return render_template('register.html', message="Error: Please fill out the highlighted fields", missing=s)
        move(5, '/')
        return render_template('register.html', message="Success! Redirecting in 5 seconds...")
    else:
        return render_template('register.html')


def move(seconds, dest):
    time.sleep(seconds)
    redirect(dest)


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/student')
def student():
    return render_template('student.html')


if __name__ == '__main__':
    app.run(port=5000, debug=False)
