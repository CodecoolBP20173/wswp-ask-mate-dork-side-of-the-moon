from flask import Flask, render_template, request, redirect, url_for

import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    data_header = data_manager.QUESTION_DATA_HEADER
    data_table = data_manager.reverse_data()
    return render_template('index.html', data_header=data_header, data_table=data_table)


@app.route('/add-question')
def route_add_question():
    pass


@app.route('/question/<question_id>')
def route_question_detail(question_id):
    question_header = data_manager.QUESTION_DATA_HEADER
    add_answer_url = url_for('route_add_answer', question_id=question_id)
    return render_template('question_detail.html', question_id=question_id, question_header=question_header, add_answer_url=add_answer_url)


@app.route('/question/<question_id>/new-answer')
def route_add_answer(question_id):
    question_header = data_manager.QUESTION_DATA_HEADER
    question_detail_url = url_for('route_question_detail', question_id=question_id)
    return render_template('add_answer.html', question_id=question_id, question_header=question_header, question_detail_url=question_detail_url)


if __name__ == '__main__':
    app.run(
        # host='0.0.0.0', TODO: uncomment this line when finished
        port=8000,
        debug=True,
    )