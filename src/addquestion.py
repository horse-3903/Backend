import sqlite3
from flask import Flask

# create sqlite connection
connection = sqlite3.connect("./database.db")
cur = connection.cursor()

# create database table
cur.execute('''CREATE TABLE IF NOT EXISTS questions(category TEXT NOT NULL, level INTEGER NOT NULL, question TEXT NOT NULL, options TEXT NOT NULL, answer INTEGER NOT NULL, explanation TEXT NOT NULL)''')

# Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>hello, world!</h1>"




question = ""
level = ""
category = ""
options = []
answer = "" #maybe ans should be like a string like option number
explanation = ""


    #yuan cheng do some html magic and make this happen

question_values = (
            (category, level, question, options, answer, explanation)
        )
def upload_to_sql():
    cur.execute("insert into questions values (category, level, question, options, answer, explanation)",question_values)


if __name__ == "__main__":
    app.run()
