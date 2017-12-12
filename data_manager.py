import connection
import os

ANSWER_DATA_FILE_PATH = os.getenv('ANSWER_DATA_FILE_PATH') if 'ANSWER_DATA_FILE_PATH' in os.environ else 'answer.csv'
QUESTION_DATA_FILE_PATH = os.getenv('QUESTION_DATA_FILE_PATH') if 'QUESTION_DATA_FILE_PATH' in os.environ else 'question.csv'
