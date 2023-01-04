from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

con = sqlite3.connect("data.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS person(name, age)")

name = input("Name of person: ")
age = input("Age of person: ")

cur.execute("""INSERT INTO person VALUES ('""" + name + """', """ + age + """)""")

con.commit()

res = cur.execute("SELECT name FROM person")

print(res.fetchall())

res = cur.execute("SELECT age FROM person")

print(res.fetchall())

age = res.fetchone()


@app.route('/')
def hello():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=5000, debug=False)
