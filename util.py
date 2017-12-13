import time
import datetime


def generate_timestamp():
    timestamp = int(time.time())
    return timestamp


def convert_timestamp_to_date(listofdict):
    for dict in listofdict:
        normaldate = datetime.datetime.fromtimestamp(float(dict['submisson_time']))
        normaldate = normaldate.strftime('%Y-%m-%d %H:%M:%S')
        dict['submisson_time'] = normaldate
    return listofdict
