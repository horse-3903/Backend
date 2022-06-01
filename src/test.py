import requests
import sqlite3
from sql_funcs import *
from extern_funcs import *
from database_columns import *

# create sqlite connection
connection = sqlite3.connect("./src/database.db", check_same_thread=False)

# debugging, set to print if need to see queries executed, set to None if hide everything
connection.set_trace_callback(print)
cur = connection.cursor()

# testing modes
QUESTION_ADD_TEST = 1
QUESTION_GET_TEST = 2
DEFINITION_ADD_TEST = 3
DEFINITION_GET_TEST = 4
USER_GET_TEST = 5
CORRECT_QUESTION_ADD_TEST = 6

# current mode (change this)
mode = USER_GET_TEST

# sample data
sample_question_data = {
    "explanation": "nothing here",
    "category": "test cat",
    "level": 2,
    "question": "helloworld",
    "option1": "blah", "option2": "another test", "option3": "this is correct", "option4": "wrong",
    "id": "test_id",
    "answer": 3,
}

sample_definition_data = {
    "item": "test",
    "definition": "testing",
    "aliases": """["testing", "tests"]""",
}

sample_correct_question_data = {
    "userid": "test userid",
    "questionid": "T001",
}

# add qn api test
if mode == QUESTION_ADD_TEST:
    r = requests.post("http://localhost:8080/api/v1/questions",
                      sample_question_data)
    print(r.text)

# get qn api test
elif mode == QUESTION_GET_TEST:
    r = requests.get("http://localhost:8080/api/v1/questions?mode=undone&num=1&userid=test%20userid")
    print(r.text)

# add definition api test
elif mode == DEFINITION_ADD_TEST:
    r = requests.post(
        "http://localhost:8080/api/v1/definitions", sample_definition_data)
    print(r.text)

elif mode == DEFINITION_GET_TEST:
    r = requests.get("http://localhost:8080/api/v1/definitions?input=tests")
    print(r.text)

elif mode == CORRECT_QUESTION_ADD_TEST:
    r = requests.post(
        "http://localhost:8080/api/v1/add_correct_question",
        sample_correct_question_data
    )
    print(r.text)

elif mode == USER_GET_TEST:
    r = requests.get(
        "http://localhost:8080/api/v1/user?userid=test%20userid"
    )
    print(r.text)