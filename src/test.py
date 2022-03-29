import requests
import sqlite3
from sql_funcs import *

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

# current mode (change this)
mode = DEFINITION_GET_TEST

# sample data
sample_question_data = safe_select(cur,"questions",{},10)

sample_definition_data = safe_select(cur,"definitions",{},10)

# add qn api test
if mode == QUESTION_ADD_TEST:
    r = requests.post("http://localhost:5000/api/v1/questions",
                      sample_question_data)
    print(r.text)

# get qn api test
elif mode == QUESTION_GET_TEST:
    r = requests.get("http://localhost:5000/api/v1/questions?mode=all&num=10")
    print(r.text)

# add definition api test
elif mode == DEFINITION_ADD_TEST:
    r = requests.post(
        "http://localhost:5000/api/v1/definitions", sample_definition_data)
    print(r.text)

elif mode == DEFINITION_GET_TEST:
    r = requests.get("http://localhost:5000/api/v1/definitions?input=tests")
    print(r.text)