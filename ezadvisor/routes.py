from flask import Flask, render_template, flash, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, logout_user, login_required
from ezadvisor import app, db
from ezadvisor.forms import LoginForm
from ezadvisor.data import Student, Advisor, Campus, Semester, Major, Courses, Catalog
from werkzeug.urls import url_parse

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
#GET and POST methods are for getting information from the web browser and posting info to the server
def login():
    if current_user.is_authenticated:
        return redirect(url_for('get_started'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(vip_id=form.username.data).first()
        advisor = Advisor.query.filter_by(vip_id=form.username.data).first()
        if (student is None or not student.check_password(form.password.data)) and (advisor is None or not advisor.check_password(form.password.data)):
            flash('The password or username you entered was invalid.')
            return redirect(url_for('login'))
        if student is None:
            login_user(advisor)
        else:
            login_user(student)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('get_started')
        return redirect(next_page)
    return render_template('index.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/get-started', methods=['GET', 'POST'])
@login_required
def get_started():
    return render_template('get-started.html')


############# Student pages ##############

@app.route('/build-schedule')
@login_required
def build_schedule():
    return render_template('build-schedule.html')


@app.route('/select-campus', methods=['GET', 'POST'])
@login_required
def select_campus():
    campuses = Campus.query.all()
    return render_template('select-campus.html', campuses=campuses)
    

@app.route('/select-term', methods=['GET', 'POST'])
@login_required
def select_term():
    terms = Semester.query.all()
    if request.method == 'POST':
        session['campus'] = request.form.get('campus')
    return render_template('select-term.html', terms=terms)


@app.route('/select-subject', methods=['GET', 'POST'])
@login_required
def select_subject():
    subject = Major.query.all()
    if request.method == 'POST':
        session['term'] = request.form.get('term')
    return render_template('select-subject.html', subject=subject)


@app.route('/search-results', methods=['GET', 'POST'])
@login_required
def search_results():
    if request.method == 'POST':
        session['subject'] = request.form.get('subject')
    courses = db.session.execute('SELECT * FROM catalog WHERE course_id in \
        (SELECT course_id FROM courses WHERE campus = :val1 AND semester = :val2 )', {'val1': session['campus'], 'val2': session['term']})
    return render_template('search-results.html', courses=courses)


@app.route('/class-sections', methods=['GET', 'POST'])
@login_required
def class_sections():
    if request.method == 'POST':
        session['course'] = request.form.get('course')
    course = session['course']
    course_id = course[0 : 9]
    course = course[11:]
    term = session['term']
    sections = db.session.execute('SELECT * FROM courses \
             WHERE campus = :val1 AND semester = :val2 AND course_id = :val3', \
            {'val1': session['campus'], 'val2': term, 'val3': course_id})
    return render_template('class-sections.html', sections=list(sections), course_id=course_id, course=course)


@app.route('/completed-schedule', methods=['GET', 'POST'])
@login_required
def completed_schedule():
    return render_template('completed-schedule.html')


@app.route('/review-schedule', methods=['GET', 'POST'])
@login_required
def review_schedule_student():
    return render_template('review-schedule.html')


@app.route('/advisor-info', methods=['GET', 'POST'])
@login_required
def advisor_info():
    advisor = db.session.execute('SELECT * FROM advisor WHERE vip_id = :val', {'val': current_user.advisor_id})
    return render_template('advisor-info.html', advisor=advisor)




############# Advisor pages ##############

@app.route('/approve-schedules')
@login_required
def approve_schedules():
    student = Student.query.filter_by(vip_id=current_user.vip_id).first()
    advisor = Advisor.query.filter_by(vip_id=current_user.vip_id).first()
    if advisor is None:
        return redirect(url_for('build_schedule'))
    return render_template('approve-schedules.html')


@app.route('/review-schedule-advisor-view')
@login_required
def review_schedule_advisor():
    return render_template('review-schedule-advisor-view.html')
