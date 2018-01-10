import time
import datetime


def get_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def initialize_view_number_and_vote_number_and_add_datetime(new_question):
    new_question.update({"view_number": 0, "vote_number": 0, "submission_time": get_datetime()})
    return new_question


def generate_timestamp():
    timestamp = int(time.time())
    return timestamp


def convert_timestamp_to_date(listofdict):
    for dict in listofdict:
        normaldate = datetime.datetime.fromtimestamp(float(dict['submisson_time']))
        normaldate = normaldate.strftime('%Y-%m-%d %H:%M:%S')
        dict['submisson_time'] = normaldate
    return listofdict
