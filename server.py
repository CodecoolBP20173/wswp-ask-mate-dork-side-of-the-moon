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
def route_question_detail():
    pass


@app.route('/question/<question_id>/new-answer')
def route_add_answer():
    pass


if __name__ == '__main__':
    app.run(
        # host='0.0.0.0', TODO: uncomment this line when finished
        port=8000,
        debug=True,
    )