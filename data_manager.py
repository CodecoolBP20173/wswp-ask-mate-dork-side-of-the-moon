import connection
import os

ANSWER_DATA_FILE_PATH = os.getenv('ANSWER_DATA_FILE_PATH') if 'ANSWER_DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
ANSWER_DATA_HEADER = ['id', 'submisson_time', 'question_id', 'message']
ANSWER_DATA_HEADER_QUESTIONS_PAGE = ['id', 'submisson_time', 'message']
QUESTION_DATA_FILE_PATH = os.getenv('QUESTION_DATA_FILE_PATH') if 'QUESTION_DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
QUESTION_DATA_HEADER = ['id', 'submisson_time', 'view_number', 'title', 'message']
FANCY_QUESTION_DATA_HEADER = ['ID', 'Submission time', 'View number', 'Title', 'Message']
QUESTION_DATA_HEADER_QUESTIONS_PAGE = ['submisson_time', 'view_number', 'title', 'message']


def reverse_data(filename):
    data = connection.csv_reader(filename)
    reversed_list = data[::-1]
    return reversed_list


def get_question_data(question_id):
    data = connection.csv_reader(QUESTION_DATA_FILE_PATH)[int(question_id)]
    return data


def get_answers_for_question(question_id):
    answers = list(connection.csv_reader(ANSWER_DATA_FILE_PATH))
    answers_for_question_id = [row for row in answers if row['question_id'] == question_id]
    return answers_for_question_id


def add_new_answer_to_csv(new_answer):
    connection.csv_appender(ANSWER_DATA_FILE_PATH, new_answer, question=False)


def get_new_answer_id():
    last_answer_id = connection.csv_reader(ANSWER_DATA_FILE_PATH)[-1]['id']
    return last_answer_id
