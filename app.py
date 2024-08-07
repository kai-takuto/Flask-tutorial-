from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///polls.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24).hex())
db = SQLAlchemy(app)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200), nullable=False)
    choices = db.relationship('Choice', backref='question', lazy=True)


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice_text = db.Column(db.String(200), nullable=False)
    votes = db.Column(db.Integer, default=0)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)


@app.route("/")
def start():
    return redirect("polls")


# /polls
@app.route('/polls/')
def polls():
    questions = Question.query.all()
    return render_template('index.html', questions=questions)


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
