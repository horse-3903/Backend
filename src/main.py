import sqlite3
from flask import Flask, request
from sql_funcs import *
from extern_funcs import *

# create sqlite connection
connection = sqlite3.connect("./src/database.db", check_same_thread = False)
connection.set_trace_callback(None) # debugging, set to print if need to see queries executed, set to None if hide everything
cur = connection.cursor()

# create database table
cur.execute('''
CREATE TABLE IF NOT EXISTS questions(category TEXT NOT NULL, level INTEGER NOT NULL, question TEXT NOT NULL,
option1 TEXT NOT NULL, option2 TEXT NOT NULL, option3 TEXT NOT NULL, option4 TEXT NOT NULL, answer INTEGER NOT NULL, explanation TEXT NOT NULL)
''')

# Flask app
app = Flask(__name__)

@app.route("/", methods = ["GET"])
def home():
    return "<h1>hello, world!</h1>"

@app.route("/api/v1/add_question", methods = ["POST"])
def add_question():

    # get post data
    content = dict(request.form)
    print(content)

    # raise error if keys not provided
    if not dictContains(("category", "level", "question", "option1", "option2", "option3", "option4", "answer", "explanation"), content):
        return "MISSING_VALUES"

    # raise error if datas are of wrong type
    if not convertDictTypes((str, int, str, str, str, str, str, int, str), content):
        return "WRONG_TYPES"

    # insert query
    safeInsert(
        cur,
        content["category"],
        content["level"],
        content["question"],
        content["option1"], content["option2"], content["option3"], content["option4"],
        content["answer"],
        content["explanation"]
    )

    # commit
    connection.commit()

    # return result
    return "SUCCESS"

if __name__ == "__main__":
    app.run()