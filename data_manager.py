import connection

FANCY_QUESTION_DATA_HEADER = ['Submission time', 'View number', 'Title', 'Message']


@connection.connection_handler
def get_question_for_index(cursor):
    cursor.execute("""
                      SELECT id, submission_time, view_number, title, message FROM question
                      ORDER BY submission_time DESC;
                      """)
    question_data = cursor.fetchall()
    return question_data


@connection.connection_handler
def get_five_last_question_for_index(cursor):
    cursor.execute("""
                      SELECT id, submission_time, view_number, title, message FROM question
                      ORDER BY submission_time DESC 
                      LIMIT 5;
                      """)
    question_data = cursor.fetchall()
    return question_data


@connection.connection_handler
def get_question_data(cursor, question_id):
    cursor.execute("""
                      SELECT submission_time, view_number, title, message FROM question
                      WHERE id = %(question_id)s;
                      """,
                   {'question_id': question_id})
    question_data = cursor.fetchall()
    return question_data


@connection.connection_handler
def get_answers_for_question(cursor, question_id):
    cursor.execute("""
                      SELECT submission_time, message FROM answer
                      WHERE question_id = %(question_id)s;
                      """,
                   {'question_id': question_id})
    answer_data = cursor.fetchall()
    return answer_data


@connection.connection_handler
def add_new_answer(cursor, new_answer):
    cursor.execute("""
                      INSERT INTO answer (submission_time, question_id, message)
                      VALUES (%(submission_time)s, %(question_id)s, %(message)s) 
                      """,
                   new_answer)


@connection.connection_handler
def increment_view_number(cursor, question_id):
    cursor.execute("""
                      UPDATE question
                      SET view_number = view_number + 1
                      WHERE id = %(question_id)s; 
                      """,
                   {'question_id': question_id})


@connection.connection_handler
def add_question(cursor, new_question):
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s)
                    """, new_question)
    cursor.execute("""
                    SELECT id FROM question
                    ORDER BY id DESC
                    LIMIT 1;
                    """)
    question_id = cursor.fetchall()
    return question_id


@connection.connection_handler
def add_new_comment(cursor, new_comment):
    cursor.execute("""
                      INSERT INTO comment (question_id, message, submission_time)
                      VALUES (%(question_id)s, %(message)s, %(submission_time)s) 
                      """,
                   new_comment)


def sort_by_time(filename):
    pass
