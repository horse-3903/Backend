import sqlite3
import json
from flask import Flask, request
from sql_funcs import *
from extern_funcs import *
from database_columns import *

# create sqlite connection
connection = sqlite3.connect("./src/database.db", check_same_thread = False)
connection.set_trace_callback(None) # debugging, set to print if need to see queries executed, set to None if hide everything
cur = connection.cursor()

# create question bank
cur.execute("""
CREATE TABLE IF NOT EXISTS questions(category TEXT NOT NULL, level INTEGER NOT NULL, question TEXT NOT NULL,
option1 TEXT NOT NULL, option2 TEXT NOT NULL, option3 TEXT NOT NULL, option4 TEXT NOT NULL, answer INTEGER NOT NULL, explanation TEXT NOT NULL, id TEXT NOT NULL)
""")

# create definition bank
cur.execute("""
CREATE TABLE IF NOT EXISTS definitions(keyword TEXT NOT NULL, aliases TEXT NOT NULL, definition TEXT NOT NULL)
""")

# create userdb
cur.execute("""
CREATE TABLE IF NOT EXISTS users(userid TEXT NOT NULL, correct_questions TEXT NOT NULL)
""")

# load layout data
with open("./src/layout.json", "r") as layout_read:
    LAYOUT_DATA = layout_read.read()

# Flask app
app = Flask(__name__)

@app.route("/", methods = ["GET"])
def home():
    return "<h1>hello, world!</h1>"

@app.route("/api/v1/layout", methods = ["GET"])
def layout():
    return LAYOUT_DATA # Return api layout. Thank me later frontend devs

@app.route("/api/v1/questions", methods = ["GET", "POST"])
def questions():

    # If the request method is POST, add question; if request method is GET return the number of questions as stated in query string
    if request.method == "POST":

        # get post data
        content = dict(request.form)

        # raise error if lacking data
        if not dictContains(QUESTION_ADD_COLUMNS, content):
            return "LACKING_DATA"

        # order dict
        orderDict(QUESTION_ADD_COLUMNS, content)

        # raise error if datas are of wrong type
        if not convertDictTypes((str, int, str, str, str, str, str, int, str), content):
            return "WRONG_TYPES"

        # insert query
        safeInsert(cur, "questions", content)

        # commit
        connection.commit()

        # return result
        return "SUCCESS"

    elif request.method == "GET":
        
        # Checks if the number of questions passed into the query string is an integer
        # The number of questions returned will correspond to the number of questions

        # get query string data
        content = dict(request.args)
        
        # raise error if lacking data
        if not dictContains(QUESTION_GET_COLUMNS, content):
            return "LACKING_DATA"

        # order dict
        orderDict(QUESTION_GET_COLUMNS, content)
        
        # raise error if datas are of wrong type
        if not convertDictTypes((str, int), content):
            return "WRONG_TYPES"

        # insert code here
        # if mode == all then find num random questions from db
        # if mode == undone then find num random questions from db that are not done

        return "SUCCESS"

@app.route("/api/v1/definitions", methods = ["GET", "POST"])
def definitions():
    
    # If request method is POST, add definition; if request method is GET return definition requested
    if request.method == "POST":
        
        # get post data
        content = dict(request.form)

        # raise error if lacking data
        if not dictContains(DEFINITION_ADD_COLUMNS, content):
            return "LACKING_DATA"
        
        # don't have to convert types, so no type checks here

        # order dict
        orderDict(DEFINITION_ADD_COLUMNS, content)

        # insert query
        safeInsert(cur, "definitions", content)

        # commit
        connection.commit()

        # return result
        return "SUCCESS"

    elif request.method == "GET":
        ... # add stuff here

if __name__ == "__main__":
    app.run()