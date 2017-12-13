import connection
import os

ANSWER_DATA_FILE_PATH = os.getenv('ANSWER_DATA_FILE_PATH') if 'ANSWER_DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
QUESTION_DATA_FILE_PATH = os.getenv('QUESTION_DATA_FILE_PATH') if 'QUESTION_DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
QUESTION_DATA_HEADER = ['id', 'submisson_time', 'view_number', 'title', 'message']


def reverse_data(filename):
    data = connection.csv_reader(filename)
    reversed_list = data[::-1]
    return reversed_list
