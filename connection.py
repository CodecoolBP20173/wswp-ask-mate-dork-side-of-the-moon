import csv
import util
import data_manager


def csv_reader_from_file(filename):
    """This function returns the database from file"""

    table = []
    with open(filename) as raw_data:
        data = csv.DictReader(raw_data)
        for line in data:
            table.append(line)
    return table



def csv_reader(filename):
    """This function modify the table from .csv file
    for jinja display"""

    table = csv_reader_from_file(filename)
    for line in table:
        for key in line:
            line[key] = line[key].replace('\n', '<br>')
            line[key] = line[key].replace('\r\n', '<br>')
            line[key] = line[key].replace('\r', '<br>')
    return table


def csv_appender(filename, dict_to_add):
    """This function appends a new input to the existing database,
    and writes the whole database back to file. Arguments:
    filename - reads the database from here, and write it back to this file.
    dict_to_add - the new input as a dictionary.
    question - if True, the input is a question, else it is an answer"""

    table = csv_reader_from_file(filename)
    if table == []:
        dict_to_add.update({"id": 1})
    else:
        dict_to_add.update({"id": int(table[-1]["id"]) + 1})
    dict_to_add.update({"submisson_time": util.generate_timestamp()})
    table.append(dict_to_add)
    write_to_file(filename, table)
    return table


def csv_updater(filename, dict_to_update):
    """This function updates the database (from filename)
    with the new information (from dict_to_update), even
    if it's a question or an answer"""

    table = csv_reader_from_file(filename)
    for line in table:
        if int(line["id"]) == int(dict_to_update["id"]) and int(line["question_id"]) == int(dict_to_update["question_id"]):
            for key in line:
                line[key] = dict_to_update[key]
        elif int(line["id"]) == int(dict_to_update["id"]):
            for key in line:
                line[key] = dict_to_update[key]
    write_to_file(filename, table)
    return table


def write_to_file(filename, table):
    """This database writes the appended or updated
    database back to file. Returns None."""

    header = table[0].keys()
    with open(filename, 'w') as raw_data:
        data = csv.DictWriter(raw_data, fieldnames=header)
        data.writeheader()
        data.writerows(table)
