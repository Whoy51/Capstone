from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

con = sqlite3.connect("data.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS person(name, age)")

name = input("Name of person: ")
age = input("Age of person: ")

cur.executemany("""INSERT INTO person VALUES (?, ?)""", [(name, age)])

con.commit()

res = cur.execute("SELECT name FROM person")

names = res.fetchall()

res = cur.execute("SELECT age FROM person")

age = res.fetchall()


print(names)
print(age)

@app.route('/')
def hello():
    return render_template('index.html', name=name, db=[names, age], names=names)


if __name__ == '__main__':
    app.run(port=5000, debug=False)
