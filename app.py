from flask import render_template, request, redirect, url_for, flash
from models import db, Question, Choice
from init import app


@app.route("/")
def start():
    return redirect("polls")


# /polls
@app.route('/polls/')
def polls():
    questions = Question.query.all()
    return render_template('index.html', question_text=questions)


# /polls/1
@app.route('/polls/<question_id>/', methods=['Get'])
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('detail.html', question=question)


# /polls/1/vote
@app.route('/polls/<int:question_id>/vote', methods=['POST'])
def vote(question_id):
    question = Question.query.get_or_404(question_id)
    choice_id = request.form.get('choice')
    if choice_id is None:
        flash('選択できていません', 'error')
        return render_template('detail.html', question=question)
    choice = Choice.query.get_or_404(choice_id)
    choice.votes += 1
    db.session.commit()

    return redirect(url_for('results', question_id=question_id))


# /polls/1/results
@app.route('/polls/<int:question_id>/results')
def results(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('results.html', question=question)
