import sqlite3

# Execute a dynamic SQL query without the risk of SQL Injections. Commiting is the responsibility of the caller.
def safeInsert(
    cursor: sqlite3.Cursor,
    category: str,
    level: int,
    question: str,
    option1: str, option2: str, option3: str, option4: str,
    answer: int,
    explanation: str
):

    # execute insert query
    cursor.execute(
    """
    INSERT INTO questions (category, level, question, option1, option2, option3, option4, answer, explanation) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        category,
        level,
        question,
        option1, option2, option3, option4,
        answer,
        explanation,
    ))