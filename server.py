from flask import Flask, render_template, request, redirect, url_for, session

import data_manager
import util
import hashing
import login

app = Flask(__name__)


@app.route('/index')
@login.login_required
def index_page():
    data_header = ['Submission time', 'View number', 'Title', 'Message']
    data_table = data_manager.get_five_last_question_for_index()
    five_questions = True
    return render_template('index.html',
                           data_header=data_header,
                           data_table=data_table,
                           five_questions=five_questions)


@app.route('/list')
@login.login_required
def route_list():
    data_header = ['Submission time', 'View number', 'Title', 'Message']
    data_table = data_manager.get_question_for_index()
    return render_template('index.html',
                           data_header=data_header,
                           data_table=data_table)


@app.route('/add-question', methods=['POST', 'GET'])
@login.login_required
def route_add_question():
    if request.method == 'POST':
        new_question = request.form.to_dict()
        new_question_add_to_database = util.initialize_view_number_and_vote_number_and_add_datetime(new_question)
        new_question_add_to_database.update({"site_user_id": session["user_id"]})
        question_id = data_manager.add_question_to_database_return_its_id(new_question_add_to_database)['id']
        return redirect(url_for('route_question_detail',
                                question_id=question_id))
    return render_template('add_question.html')


@app.route('/question/<question_id>')
@login.login_required
def route_question_detail(question_id):
    data_manager.increment_view_number(question_id)
    question_data = data_manager.get_question_data(question_id)
    answers = data_manager.get_answers_for_question(question_id)
    question_comments = data_manager.get_comments_for_question(question_id)
    answer_comments = data_manager.get_answer_comments()
    answer_id_list_for_comments = [row['answer_id'] for row in answer_comments]
    add_answer_url = url_for('route_add_answer', question_id=question_id)
    logged_in = session['user_id']
    return render_template('question_detail.html',
                           question_id=question_id,
                           add_answer_url=add_answer_url,
                           question_data=question_data,
                           answers=answers,
                           question_comments=question_comments,
                           answer_comments=answer_comments,
                           answer_id_list_for_comments=answer_id_list_for_comments,
                           logged_in=logged_in,
                           session_user=session["user_name"])


@app.route('/question/<question_id>/new-answer', methods=['POST', 'GET'])
@login.login_required
def route_add_answer(question_id):
    question_detail_url = url_for('route_question_detail', question_id=question_id)
    if request.method == 'POST':
        new_answer = request.form.to_dict()
        new_answer['submission_time'] = util.get_datetime()
        new_answer['site_user_id'] = session['user_id']
        data_manager.add_new_answer(new_answer)
        return redirect(question_detail_url)

    question_data = data_manager.get_question_data(question_id)
    answers = data_manager.get_answers_for_question(question_id)
    add_answer_url = url_for('route_add_answer', question_id=question_id)
    return render_template('add_answer.html',
                           question_id=question_id,
                           add_answer_url=add_answer_url,
                           question_data=question_data,
                           answers=answers)


@app.route('/search-question', methods=['GET'])
@login.login_required
def search_question():
    data_header = ['Submission time', 'View number', 'Title', 'Message']
    search_phrase = request.args.get('q')
    questions = data_manager.search_questions(search_phrase)
    five_questions = True
    return render_template('index.html',
                           data_header=data_header,
                           data_table=questions,
                           five_questions=five_questions)


@app.route('/question/<question_id>/new-comment', methods=['POST', 'GET'])
@login.login_required
def add_question_comment(question_id):
    question_detail_url = url_for('route_question_detail', question_id=question_id)
    if request.method == 'POST':
        new_comment = request.form.to_dict()
        new_comment = util.initialize_view_number_and_vote_number_and_add_datetime(new_comment)
        new_comment.update({'site_user_id': session['user_id']})
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
@login.login_required
def add_answer_comment(answer_id):
    question_detail_url = url_for('route_question_detail',
                                  question_id=data_manager.get_question_id_for_answer(answer_id)['question_id'])
    if request.method == 'POST':
        new_comment = request.form.to_dict()
        new_comment['submission_time'] = util.get_datetime()
        new_comment.update({'site_user_id': session['user_id']})
        data_manager.add_new_answer_comment(new_comment)
        return redirect(question_detail_url)

    answer_data = data_manager.get_answer_data(answer_id)
    add_comment_url = url_for('add_answer_comment', answer_id=answer_id)
    return render_template('add_comment_answer.html',
                           answer_id=answer_id,
                           question_detail_url=question_detail_url,
                           add_comment_url=add_comment_url,
                           answer_data=answer_data)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
@login.login_required
def modify_question(question_id):
    question = data_manager.get_question_data(question_id)
    if question["user_name"] == session["user_name"]:
        if request.method == 'POST':
            question_to_update = request.form.to_dict()
            data_manager.edit_question(question_to_update)
            return redirect(url_for('route_question_detail',
                                    question_id=question_id))
        return render_template('add_question.html',
                               question=question,
                               question_id=question_id)
    
    return redirect("https://i.imgflip.com/239qx5.jpg")


@app.route('/question/<question_id>/delete', methods=['POST', 'GET'])
@login.login_required
def delete_question(question_id):
    question = data_manager.get_question_data(question_id)
    if question["user_name"] == session["user_name"]:
        data_manager.delete_question_and_its_answers(question_id)
        return redirect('/')
    return redirect("https://i.imgflip.com/239qx5.jpg")


@app.route('/answer/<answer_id>/edit', methods=['POST', 'GET'])
@login.login_required
def route_edit_answer(answer_id):
    if request.method == 'POST':
        answer_to_update = request.form.to_dict()
        question_id = data_manager.get_question_id_for_answer(answer_id)['question_id']
        data_manager.edit_answer(answer_to_update)
        return redirect(url_for('route_question_detail', question_id=question_id))
    answer = data_manager.get_answer_data(answer_id)
    logged_in = session['user_id']
    owner_id = answer['site_user_id']
    if logged_in == owner_id:
        return render_template('edit_answer.html',
                               answer_id=answer_id,
                               answer=answer)
    else:
        return redirect('https://i.imgflip.com/239qx5.jpg')


@app.route('/comments/<comment_id>/delete', methods=['POST', 'GET'])
@login.login_required
def delete_comment(comment_id):
    site_user_id = data_manager.get_site_user_id_by_comment_id(comment_id)
    if site_user_id['site_user_id'] != session['user_id']:
        return redirect('https://i.imgflip.com/239qx5.jpg')
    question_id = str(data_manager.get_question_id_by_comment_id(comment_id)['question_id'])
    if question_id == 'None':
        answer_id = data_manager.get_answer_id_by_comment_id(comment_id)['answer_id']
        question_id = str(data_manager.get_question_id_by_answer_id(answer_id)['question_id'])

    data_manager.delete_comment(comment_id)
    return redirect('/question/' + question_id)


@app.route('/comments/<comment_id>/edit', methods=['POST', 'GET'])
@login.login_required
def update_comment(comment_id):
    site_user_id = data_manager.get_site_user_id_by_comment_id(comment_id)
    if site_user_id['site_user_id'] != session['user_id']:
        return redirect('https://i.imgflip.com/239qx5.jpg')
    if request.method == 'POST':
        comment_to_update = request.form.to_dict()
        data_manager.edit_comment(comment_to_update)
        question_id = str(data_manager.get_question_id_by_comment_id(comment_id)['question_id'])
        return redirect('/question/'+question_id)

    comment = data_manager.get_comment_by_id(comment_id)
    return render_template('edit_comment.html',
                           comment_id=comment_id,
                           comment=comment)


@app.route('/user_list')
@login.login_required
def user_list():
    user_data = data_manager.get_user_data()
    return render_template('user_list.html',
                           user_data=user_data)

  
@app.route('/', methods=['POST', 'GET'])
def sign_up_screen():

    sign_up_message = ""
    login_message = ""

    if request.method == 'POST':
        new_user_data = request.form.to_dict()

        if "new_user_name" in new_user_data:
            new_user_data["new_password"] = hashing.hash_password(new_user_data["new_password"])
            unsuccessful_sign_up = data_manager.sign_up(new_user_data)

            if unsuccessful_sign_up is True:
                sign_up_message = "Username taken. Enter another name."
                return render_template('login.html',
                                       sign_up_message = sign_up_message,
                                       login_message=login_message)

            else:
                sign_up_message = "Sign up successful. Login allowed"
                return render_template('login.html',
                                       sign_up_message = sign_up_message,
                                       login_message=login_message)

        else:
            login_data = request.form.to_dict()
            unhashed_password = login_data['password']
            user_name = login_data['user_name']
            hashed_password_dict = data_manager.get_hashed_password_by_user_name(user_name)

            if hashed_password_dict is None:
                login_message = "Incorrect user name or password."
                return render_template('login.html',
                                       sign_up_message=sign_up_message,
                                       login_message=login_message)

            else:
                hashed_password = hashed_password_dict['password']
                verified = hashing.verify_password(unhashed_password, hashed_password)

                if verified:
                    session['user_id'] = data_manager.get_id_by_user_name(user_name)['id']
                    session['user_name'] = login_data['user_name']
                    return redirect(url_for('index_page'))

                else:
                    login_message = "Incorrect user name or password."

    return render_template('login.html',
                           sign_up_message = sign_up_message,
                           login_message=login_message)


@app.route('/logout')
@login.login_required
def logout():
    session.clear()
    return redirect(url_for('sign_up_screen'))


if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
