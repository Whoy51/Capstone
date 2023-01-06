from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

con = sqlite3.connect("data.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(studentid, name, teacher)")


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
        print(request.form['studentid'])
        print(request.form['teacher'])
        return render_template('register.html', message="Registration Success!")
    return render_template('register.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/student')
def student():
    return render_template('student.html')


if __name__ == '__main__':
    app.run(port=5000, debug=False)
