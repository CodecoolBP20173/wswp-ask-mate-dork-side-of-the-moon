import connection


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

def sort_by_time(filename):
    pass
