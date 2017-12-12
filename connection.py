import csv


def csv_reader(filename):
    """This function returns the database from file"""

    table = []
    with open(filename) as raw_data:
        data = csv.DictReader(raw_data)
        for line in data:
            table.append(line)
    return table


def csv_appender(filename, dict_to_add, question=True):
    """This function appends a new input to the existing database,
    and writes the whole database back to file. Arguments:
    filename - reads the database from here, and write it back to this file.
    dict_to_add - the new input as a dictionary.
    question - if True, the input is a question, else it is an answer"""

    table = csv_reader(filename)
    if table == [] and question:
        dict_to_add.update({"id": 1})
    elif question:
        dict_to_add.update({"id": int(table[-1]["id"]) + 1})
    elif table == [] and not question:
        dict_to_add.update({"a_id": 1})
    else:
        answer_id_list = []
        for line in table:
            if line["id"] == dict_to_add["id"]:
                answer_id_list.append(int(dict_to_add["a_id"]))
        dict_to_add.update({"a_id": max(answer_id_list) + 1})
    table.append(dict_to_add)
    write_to_file(filename, table)
    return table


def csv_updater(filename, dict_to_update):
    """This function updates the database (from filename)
    with the new information (from dict_to_update), even
    if it's a question or an answer"""

    table = csv_reader(filename)
    for line in table:
        if int(line["a_id"]) == int(dict_to_update["a_id"]) and int(line["id"]) == int(dict_to_update["id"]):
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
