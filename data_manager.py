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
def get_answer_data(cursor, answer_id):
    cursor.execute("""
                      SELECT submission_time, message FROM answer
                      WHERE id = %(answer_id)s;
                      """,
                   {'answer_id': answer_id})
    answer_data = cursor.fetchall()
    return answer_data


@connection.connection_handler
def get_answers_for_question(cursor, question_id):
    cursor.execute("""
                      SELECT submission_time, message, id FROM answer
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
def search_questions(cursor, search_phrase):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE title LIKE %(search)s OR message LIKE %(search)s;
                    """, {'search': '%' + search_phrase + '%'})
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def add_new_comment(cursor, new_comment):
    cursor.execute("""
                      INSERT INTO comment (question_id, message, submission_time, site_user_id)
                      VALUES (%(question_id)s, %(message)s, %(submission_time)s, %(site_user_id)s); 
                      """,
                   new_comment)


@connection.connection_handler
def add_new_answer_comment(cursor, new_comment):
    cursor.execute("""
                      INSERT INTO comment (answer_id, message, submission_time, site_user_id)
                      VALUES (%(answer_id)s, %(message)s, %(submission_time)s, %(site_user_id)s) 
                    """,
                   new_comment)


@connection.connection_handler
def get_comments_for_question(cursor, question_id):
    cursor.execute("""
                    SELECT submission_time, message, id FROM comment
                    WHERE question_id = %(question_id)s;
                   """,
                   {'question_id': question_id})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def get_answer_comments(cursor):
    cursor.execute("""
                    SELECT submission_time, message, answer_id, id FROM comment
                   """)
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def get_question_id_for_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id FROM answer
                    WHERE id = %(answer_id)s;
                   """,
                   {'answer_id': answer_id})
    question_id = cursor.fetchall()
    return question_id


@connection.connection_handler
def edit_question(cursor, question):
    cursor.execute("""
                      UPDATE question
                      SET title = %(title)s, message = %(message)s
                      WHERE id = %(id)s;
                    """,
                   question)


@connection.connection_handler
def delete_question_and_its_answers(cursor, question_id):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE question_id = %(id_to_delete)s;
                    """, {'id_to_delete': question_id})

    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(id_to_delete)s;
                    """, {'id_to_delete': question_id})


@connection.connection_handler
def edit_answer(cursor, answer):
    cursor.execute("""
                    UPDATE answer
                    SET message = %(message)s
                    WHERE id = %(id)s;
                    """,
                   answer)


@connection.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id=%(comment_id)s;
                   """,
                   {'comment_id': comment_id})


@connection.connection_handler
def get_question_id_by_comment_id(cursor, comment_id):
    cursor.execute("""
                    SELECT question_id, answer_id FROM comment
                    WHERE id = %(comment_id)s;
                   """,
                   {'comment_id': comment_id})
    comment_id = cursor.fetchall()
    return comment_id


@connection.connection_handler
def get_question_id_by_answer_id(cursor, id):
    cursor.execute("""
                    SELECT question_id FROM answer
                    WHERE id = %(id)s;
                   """,
                   {'id': id})
    comment_id = cursor.fetchall()
    return comment_id


@connection.connection_handler
def get_answer_id_by_comment_id(cursor, comment_id):
    cursor.execute("""
                    SELECT answer_id FROM comment
                    WHERE id = %(comment_id)s;
                   """,
                   {'comment_id': comment_id})
    comment_id = cursor.fetchall()
    return comment_id


@connection.connection_handler
def get_comment_by_id(cursor, comment_id):
    cursor.execute("""
                    SELECT id, message, edited_count
                    FROM comment
                    WHERE id = %(id)s;
                    """,
                   {'id' : comment_id})
    return cursor.fetchone()


@connection.connection_handler
def edit_comment(cursor, comment):
    cursor.execute("""
                    UPDATE comment
                    SET message = %(message)s
                    WHERE id = %(id)s;
                    """,
                   comment)


@connection.connection_handler
def get_user_data(cursor):
    cursor.execute("""
                      SELECT id, user_name, registration_date FROM site_user;
                      """)
    user_data = cursor.fetchall()
    return user_data


@connection.connection_handler
def get_hashed_password_by_user_name(cursor, user_name):
    cursor.execute("""
                    SELECT password FROM site_user
                    WHERE user_name = %(user_name)s;
                   """,
                   {'user_name': user_name})
    password = cursor.fetchone()
    return password


@connection.connection_handler
def sign_up(cursor, new_user_data):
    try:
        cursor.execute("""
                      INSERT INTO site_user (user_name, password)
                      VALUES (%(new_user_name)s, %(new_password)s)
                      """, new_user_data);
        return False
    except:
        return True


@connection.connection_handler
def get_id_by_user_name(cursor, user_name):
    cursor.execute("""
                    SELECT id FROM site_user
                    WHERE user_name = %(user_name)s;
                   """,
                   {'user_name': user_name})
    id = cursor.fetchone()
    return id
