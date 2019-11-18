from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, logout_user, login_required
from ezadvisor import app
from ezadvisor.forms import LoginForm, CampusForm, TermForm
from ezadvisor.data import Student


@app.route('/login', methods=['GET', 'POST'])
#GET and POST methods are for getting information from the web browser and posting info to the server
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(name=form.username.data).first()
        if student is None or not student.password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            login_user(student)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)

@app.route('/login')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/get-started')
@login_required
def get_started():
    return render_template('get-started.html')


@app.route('/build-schedule')
@login_required
def build_schedule():
    return render_template('build-schedule.html')


@app.route('/select-campus', methods=['GET', 'POST'])
@login_required
def select_campus():
    form = CampusForm()
    return render_template('select-campus.html', form=form)
    

@app.route('/select-term', methods=['GET', 'POST'])
@login_required
def select_term():
    form = TermForm()
    return render_template('select-term.html', form=form)


@app.route('/select-subject', methods=['GET', 'POST'])
@login_required
def select_subject():
    return render_template('select-subject.html')
