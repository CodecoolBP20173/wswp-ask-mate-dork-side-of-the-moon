from flask import Flask, render_template, request, redirect, url_for

import data_manager
import connection
import util

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    question_file = data_manager.QUESTION_DATA_FILE_PATH
    data_header = data_manager.FANCY_QUESTION_DATA_HEADER
    data_table = data_manager.sort_by_time(question_file)
    data_table = util.convert_timestamp_to_date(data_table)
    return render_template('index.html', data_header=data_header, data_table=data_table)


@app.route('/add-question', methods=['POST', 'GET'])
def route_add_question():
    if request.method == 'POST':
        new_question = request.form.to_dict()
        connection.csv_appender('sample_data/question.csv', new_question)
        return redirect(url_for('route_question_detail',
                                question_id=connection.csv_reader('sample_data/question.csv')[-1]["id"]))
    return render_template('/add_question.html')


@app.route('/question/<question_id>')
def route_question_detail(question_id):
    question_header = data_manager.QUESTION_DATA_HEADER_QUESTIONS_PAGE
    question_header_display = data_manager.make_display_header(question_header)
    data_manager.increment_view_number(question_id)
    question_data = data_manager.get_question_data(question_id)
    answer_header = data_manager.ANSWER_DATA_HEADER_QUESTIONS_PAGE
    answer_header_display = data_manager.make_display_header(answer_header)
    answers = data_manager.get_answers_for_question(question_id)
    add_answer_url = url_for('route_add_answer', question_id=question_id)
    return render_template('question_detail.html',
                           question_id=question_id,
                           question_header=question_header,
                           add_answer_url=add_answer_url,
                           question_data=question_data,
                           answer_header=answer_header,
                           answers=answers,
                           question_header_display=question_header_display,
                           answer_header_display=answer_header_display)


@app.route('/question/<question_id>/new-answer', methods=['POST', 'GET'])
def route_add_answer(question_id):
    question_detail_url = url_for('route_question_detail', question_id=question_id)
    if request.method == 'POST':
        new_answer = request.form.to_dict()
        data_manager.add_new_answer_to_csv(new_answer)
        return redirect(question_detail_url)
    
    question_header = data_manager.QUESTION_DATA_HEADER_QUESTIONS_PAGE
    question_header_display = data_manager.make_display_header(question_header)
    question_data = data_manager.get_question_data(question_id)
    answer_header = data_manager.ANSWER_DATA_HEADER_QUESTIONS_PAGE
    answer_header_display = data_manager.make_display_header(answer_header)
    answers = data_manager.get_answers_for_question(question_id)
    add_answer_url = url_for('route_add_answer', question_id=question_id)
    return render_template('add_answer.html',
                           question_id=question_id,
                           question_header=question_header,
                           add_answer_url=add_answer_url,
                           question_data=question_data,
                           answer_header=answer_header,
                           answers=answers,
                           question_header_display=question_header_display,
                           answer_header_display=answer_header_display)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
