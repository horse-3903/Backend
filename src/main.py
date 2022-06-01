import sqlite3
import json
import random
from flask import Flask, request
from sql_funcs import *
from extern_funcs import *
from database_columns import *

"""
Do not add HTML in the returned value
Changed test values back to fixed dictionaries
TAB = 2 space not 4
Follow pep8 formatting
TEST YOUR CODE! SO MANY BUGS
"""

# create sqlite connection
connection = sqlite3.connect("./src/database.db", check_same_thread=False)

# debugging, set to print if need to see queries executed, set to None if hide everything
connection.set_trace_callback(None)
cur = connection.cursor()

# create question bank
cur.execute("""
CREATE TABLE IF NOT EXISTS questions(category TEXT NOT NULL, level INTEGER NOT NULL, question TEXT NOT NULL,
option1 TEXT NOT NULL, option2 TEXT NOT NULL, option3 TEXT NOT NULL, option4 TEXT NOT NULL, answer INTEGER NOT NULL, explanation TEXT NOT NULL, id TEXT NOT NULL UNIQUE)
""")

# create definition bank
cur.execute("""
CREATE TABLE IF NOT EXISTS definitions(item TEXT NOT NULL, definition TEXT NOT NULL, aliases TEXT NOT NULL)
""")

# create userdb
cur.execute("""
CREATE TABLE IF NOT EXISTS users(userid TEXT NOT NULL UNIQUE, correct_questions TEXT NOT NULL)
""")

# load layout data
with open("./src/layout.json", "r") as layout_read:
    LAYOUT_DATA = layout_read.read()

# Flask app
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "CONNECTION_SUCESS"

@app.route("/api/v1/layout", methods=["GET"])
def layout():
    return LAYOUT_DATA  # Return api layout. Thank me later frontend devs

@app.route("/api/v1/questions", methods=["GET", "POST"])
def questions():

    # If the request method is POST, add question; if request method is GET return the number of questions as stated in query string
    if request.method == "POST":

        # get post data
        content = dict(request.form)

        # raise error if lacking data
        if not dict_contains(QUESTION_ADD_COLUMNS, content):
            return "LACKING_DATA"

        # order dict
        order_dict(QUESTION_ADD_COLUMNS, content)

        # raise error if datas are of wrong type
        if not convert_dict_types((str, int, str, str, str, str, str, int, str, str), content):
            return "WRONG_TYPES"

        # insert query
        safe_insert(cur, "questions", content)

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
        if not dict_contains(QUESTION_GET_COLUMNS, content):
            return "LACKING_DATA"

        # order dict
        order_dict(QUESTION_GET_COLUMNS, content)

        # raise error if datas are of wrong type
        if not convert_dict_types((str, int, str), content):
            return "WRONG_TYPES"

        # insert code here
        # if mode == all then find num random questions from db
        if content["mode"] == "all":
            data = safe_select(cur,"questions",{},content["num"])
            random.shuffle(data)
            return json.dumps(data)
            
        # if mode == undone then find num random questions from db that are not in user list of correct questions
        elif content["mode"] == "undone":
            questions = json.loads(safe_select(cur, "users", {"userid = ?": content["userid"]}, 1)[0][1])
            data = safe_select(cur, "questions", {f"id NOT IN ({', '.join('?' for q in questions)})": questions}, 1, "list(select_dict.values())[0]")
            random.shuffle(data)
            return json.dumps(data)
        
        return "INVALID_MODE"

@app.route("/api/v1/definitions", methods=["GET", "POST"])
def definitions():

    # If request method is POST, add definition; if request method is GET return definition requested
    if request.method == "POST":

        # get post data
        content = dict(request.form)

        # raise error if lacking data
        if not dict_contains(DEFINITION_ADD_COLUMNS, content):
            return "LACKING_DATA"

        # don't have to convert types, so no type checks here

        # order dict
        order_dict(DEFINITION_ADD_COLUMNS, content)

        # insert query
        safe_insert(cur, "definitions", content)

        # commit
        connection.commit()

        # return result
        return "SUCCESS"

    elif request.method == "GET":
        
        # get query string params
        content = dict(request.args)

        # raise error if lacking data
        if not dict_contains(DEFINITION_GET_COLUMNS, content):
            return "LACKING_DATA"

        # don't have to convert types / order dict, so nothing here

        # get all definitions
        all_definitions = safe_select(cur, "definitions", {}, 10000000000)

        # find which definitions match
        for definition in all_definitions:
            aliases = json.loads(definition[2])
            aliases.append(definition[0]) # add the main definition name as well
            if content["input"] in aliases:
                return to_json(DEFINITION_ADD_COLUMNS, [*definition[:-1], json.loads(definition[-1])]) # return definition
 
        # wasnt found
        return "NOT_FOUND"

@app.route("/api/v1/user", methods=["GET"])
def users():

    # check if input data is in database when user runs command 
    content = dict(request.args)

    if not dict_contains(USER_GET_COLUMNS, content):
        return "LACKING_DATA"

    data = safe_select(cur,"users",{"userid = ?":content["userid"]}, 1)

    if not data:
        return "NOT_FOUND"
    else:
        data = data[0]
        return to_json(("userid", "correct_questions"), [*data[:-1], json.loads(data[-1])])

@app.route("/api/v1/add_correct_question", methods=["POST"])
def add_correct_question():

    """
    Might need a way to verify that the user actually did the question,
    if not trolls can just send an API request to give people more correct questions
    """

    # get post data
    content = dict(request.form)

    # raise error if lacking data
    if not dict_contains(CORRECT_QUESTION_ADD_COLUMNS, content):
        return "LACKING_DATA"

    # order dict
    order_dict(CORRECT_QUESTION_ADD_COLUMNS, content)

    # don't have to convert types so nothing here

    # add user by userid into the database if not exists
    if not safe_select(cur, "users", {"userid = ?": content["userid"]}, 1):
        safe_insert(cur, "users", {"userid": content["userid"], "correct_questions": "[]"})

    # add the question into the done questions for user
    current_user_done = json.loads(
        safe_select(cur, "users", {"userid = ?": content["userid"]}, 1)[0][1]
    )
    current_user_done.append(content["questionid"])
    safe_update(cur, "users", {"correct_questions = ?": json.dumps(current_user_done)}, {"userid = ?": content["userid"]})

    connection.commit()

    return "SUCCESS"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")
