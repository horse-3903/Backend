import sqlite3
from flask import Flask

# create sqlite connection
connection = sqlite3.connect("./src/database.db")
cur = connection.cursor()

# create database table
cur.execute('''CREATE TABLE IF NOT EXISTS questions(category TEXT NOT NULL, level INTEGER NOT NULL, question TEXT NOT NULL, 
                options TEXT NOT NULL, answer INTEGER NOT NULL, explanation TEXT NOT NULL)''')

# Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>hello, world!</h1>"

if __name__ == "__main__":
    app.run()