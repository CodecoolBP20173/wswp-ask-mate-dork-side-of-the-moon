from flask import Flask, render_template, request, redirect, url_for

import data_manager
import connection
import util

app = Flask(__name__)


@app.route('/')
def index_page():
    data_header = data_manager.FANCY_QUESTION_DATA_HEADER
    data_table = data_manager.get_five_last_question_for_index()
    five_questions = True
    return render_template('index.html', data_header=data_header, data_table=data_table, five_questions=five_questions)


@app.route('/list')
def route_list():
    data_header = data_manager.FANCY_QUESTION_DATA_HEADER
    data_table = data_manager.get_question_for_index()
    return render_template('index.html', data_header=data_header, data_table=data_table)


@app.route('/add-question', methods=['POST', 'GET'])
def route_add_question():
    if request.method == 'POST':
        new_question = request.form.to_dict()
        new_question_add_to_database = util.initialize_view_number_and_vote_number_and_add_datetime(new_question)
        question_id = data_manager.add_question(new_question_add_to_database)[0]['id']
        return redirect(url_for('route_question_detail',
                                question_id=question_id))
    return render_template('/add_question.html')


@app.route('/question/<question_id>')
def route_question_detail(question_id):
    data_manager.increment_view_number(question_id)
    question_data = data_manager.get_question_data(question_id)[0]
    answers = data_manager.get_answers_for_question(question_id)
    question_comments = data_manager.get_comments_for_question(question_id)
    answer_comments = data_manager.get_answer_comments()
    answer_id_list_for_comments = [row['answer_id'] for row in answer_comments]
    add_answer_url = url_for('route_add_answer', question_id=question_id)
    return render_template('question_detail.html',
                           question_id=question_id,
                           add_answer_url=add_answer_url,
                           question_data=question_data,
                           answers=answers,
                           question_comments=question_comments,
                           answer_comments=answer_comments,
                           answer_id_list_for_comments=answer_id_list_for_comments)


@app.route('/question/<question_id>/new-answer', methods=['POST', 'GET'])
def route_add_answer(question_id):
    question_detail_url = url_for('route_question_detail', question_id=question_id)
    if request.method == 'POST':
        new_answer = request.form.to_dict()
        new_answer['submission_time'] = util.get_datetime()
        data_manager.add_new_answer(new_answer)
        return redirect(question_detail_url)

    question_data = data_manager.get_question_data(question_id)[0]
    answers = data_manager.get_answers_for_question(question_id)
    add_answer_url = url_for('route_add_answer', question_id=question_id)
    return render_template('add_answer.html',
                           question_id=question_id,
                           add_answer_url=add_answer_url,
                           question_data=question_data,
                           answers=answers)


@app.route('/search-question', methods=['GET'])
def search_question():
    data_header = data_manager.FANCY_QUESTION_DATA_HEADER
    search_phrase = request.args.get('q')
    questions = data_manager.search_questions(search_phrase)
    five_questions = True
    return render_template('index.html',
                           data_header=data_header,
                           data_table=questions,
                           five_questions=five_questions)


@app.route('/question/<question_id>/new-comment', methods=['POST', 'GET'])
def add_question_comment(question_id):
    question_detail_url = url_for('route_question_detail', question_id=question_id)
    if request.method == 'POST':
        new_comment = request.form.to_dict()
        new_comment = util.initialize_view_number_and_vote_number_and_add_datetime(new_comment)
        data_manager.add_new_comment(new_comment)
        return redirect(question_detail_url)
    add_question_comment_url = url_for('add_question_comment', question_id=question_id)
    question = data_manager.get_question_data(question_id)
    data_header = ['Submission time', 'Title', 'Message']
    return render_template('add_comment_question.html',
                           add_question_comment_url=add_question_comment_url,
                           question=question,
                           data_header=data_header,
                           question_id=question_id)


@app.route('/answer/<answer_id>/new-comment', methods=['POST', 'GET'])
def add_answer_comment(answer_id):
    question_detail_url = url_for('route_question_detail', question_id=data_manager.get_question_id_for_answer(answer_id)[0]['question_id'])
    if request.method == 'POST':
        new_comment = request.form.to_dict()
        new_comment['submission_time'] = util.get_datetime()
        data_manager.add_new_answer_comment(new_comment)
        return redirect(question_detail_url)

    answer_data = data_manager.get_answer_data(answer_id)[0]
    add_comment_url = url_for('add_answer_comment', answer_id=answer_id)
    return render_template('add_comment_answer.html',
                           answer_id=answer_id,
                           question_detail_url=question_detail_url,
                           add_comment_url=add_comment_url,
                           answer_data=answer_data)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def modify_question(question_id):
    if request.method == 'POST':
        question_to_update = request.form.to_dict()
        data_manager.edit_question(question_to_update)
        return redirect(url_for('route_question_detail',
                                question_id=question_id))
    question = data_manager.get_question_data(question_id)[0]
    return render_template('add_question.html',
                           question=question,
                           question_id=question_id)


@app.route('/question/<question_id>/delete', methods=['POST', 'GET'])
def delete_question(question_id):
    data_manager.delete_question_and_its_answers(question_id)
    return redirect('/')


@app.route('/answer/<answer_id>/edit', methods=['POST', 'GET'])
def route_edit_answer(answer_id):
    if request.method == 'POST':
        answer_to_update = request.form.to_dict()
        question_id = data_manager.get_question_id_for_answer(answer_id)[0]['question_id']
        data_manager.edit_answer(answer_to_update)
        return redirect(url_for('route_question_detail', question_id = question_id))
    answer = data_manager.get_answer_data(answer_id)[0]
    return render_template('edit_answer.html', answer_id = answer_id, answer = answer)


@app.route('/comments/<comment_id>/delete', methods=['POST', 'GET'])
def delete_comment(comment_id):
    question_id = str(data_manager.get_question_id_by_comment_id(comment_id)[0]['question_id'])
    if question_id == 'None':
        answer_id = data_manager.get_answer_id_by_comment_id(comment_id)[0]['answer_id']
        question_id = str(data_manager.get_question_id_by_answer_id(answer_id)[0]['question_id'])

    data_manager.delete_comment(comment_id)
    return redirect('/question/' + question_id)


@app.route('/comments/<comment_id>/edit', methods=['POST', 'GET'])
def update_comment(comment_id):
    if request.method == 'POST':
        comment_to_update = request.form.to_dict()
        data_manager.edit_comment(comment_to_update)
        question_id = str(data_manager.get_question_id_by_comment_id(comment_id)[0]['question_id'])
        return redirect('/question/'+question_id)
    comment = data_manager.get_comment_by_id(comment_id)
    return render_template('edit_comment.html', comment_id = comment_id, comment = comment)


@app.route('/user_list')
def user_list():
    user_data = data_manager.get_user_data()
    return render_template('user_list.html', user_data=user_data)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
