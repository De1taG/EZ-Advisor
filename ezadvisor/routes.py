from flask import Flask, render_template, flash, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, logout_user, login_required
from ezadvisor import app, db
from ezadvisor.forms import LoginForm
from ezadvisor.data import Student, Advisor, Campus, Semester, Major, Courses, Catalog, proposedSchedule, submittedSchedules
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
    if request.method == 'POST':
        session['campus'] = request.form.get('campus')
        return redirect(url_for('select_term'))
    return render_template('select-campus.html', campuses=campuses)
    

@app.route('/select-term', methods=['GET', 'POST'])
@login_required
def select_term():
    terms = Semester.query.all()
    if request.method == 'POST':
        session['term'] = request.form.get('term')
        return redirect(url_for('select_subject'))
    return render_template('select-term.html', terms=terms)


@app.route('/select-subject', methods=['GET', 'POST'])
@login_required
def select_subject():
    subject = Major.query.all()
    if request.method == 'POST':
        session['subject'] = request.form.get('subject')
        return redirect(url_for('search_results'))
    return render_template('select-subject.html', subject=subject)


@app.route('/search-results', methods=['GET', 'POST'])
@login_required
def search_results():
    if request.method == 'POST':
        session['course'] = request.form.get('course')
        return redirect(url_for('class_sections'))
    courses = db.session.execute('SELECT * FROM catalog WHERE course_id in \
        (SELECT course_id FROM courses WHERE campus = :val1 AND semester = :val2 )', {'val1': session['campus'], 'val2': session['term']})
    return render_template('search-results.html', courses=courses)


@app.route('/class-sections', methods=['GET', 'POST'])
@login_required
def class_sections():
    if request.method == 'POST':
        flash('Course successfully added!', 'dark')
        crn = request.form.get('course_crn')
        semester = request.form.get('course_semester')
        new_course = proposedSchedule(student_vip_id = current_user.vip_id, course_crn = crn, semester=semester)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('class_sections'))
    course = session['course']
    course_id = course[0 : 9]
    course = course[11:]
    sections = db.session.execute('SELECT * FROM courses \
             WHERE campus = :val1 AND semester = :val2 AND course_id = :val3', \
            {'val1': session['campus'], 'val2': session['term'], 'val3': course_id})
    return render_template('class-sections.html', sections=list(sections), course_id=course_id, course=course)


@app.route('/completed-schedule', methods=['GET', 'POST'])
@login_required
def completed_schedule():
    classes = db.session.execute('SELECT courses.* FROM proposed_schedule \
        left JOIN courses on proposed_schedule.course_crn = courses.crn \
        where proposed_schedule.student_vip_id = :val1 and proposed_schedule.semester= :val2', \
        {'val1': current_user.vip_id, 'val2': session['term']})
    hours = db.session.execute('SELECT sum(courses.credit_hours) as sum FROM proposed_schedule \
        left JOIN courses on proposed_schedule.course_crn = courses.crn \
        where proposed_schedule.student_vip_id = :val1 and proposed_schedule.semester= :val2', \
        {'val1': current_user.vip_id, 'val2': session['term']})
    if request.method == 'POST':
        total_hours = request.form.get('total_hours')
        if total_hours == '0':
            flash('Error: You cannot submit a schedule with zero classes added.', 'danger')
        else:
            flash('Your schedule has been submitted to your advisor for feedback!', 'dark')
            semester = session['term']
            new_schedule = submittedSchedules(student_vip_id = current_user.vip_id, advisor_vip_id = current_user.advisor_id, semester = semester, status = 'Needs Review')
            db.session.add(new_schedule)
            db.session.commit()
        return redirect(url_for('review_schedule_student'))
    return render_template('completed-schedule.html', classes=list(classes), hours=hours.first(), semester=session['term'])


@app.route('/review-schedule', methods=['GET', 'POST'])
@login_required
def review_schedule_student():
    classes = db.session.execute('SELECT courses.* FROM proposed_schedule \
        left JOIN courses on proposed_schedule.course_crn = courses.crn \
        where proposed_schedule.student_vip_id = :val1 and proposed_schedule.semester= :val2', \
        {'val1': current_user.vip_id, 'val2': session['term']})
    hours = db.session.execute('SELECT (case when sum(courses.credit_hours) > 0 then sum(courses.credit_hours) else 0 end) \
        as "sum"  FROM proposed_schedule \
        left JOIN courses on proposed_schedule.course_crn = courses.crn \
        where proposed_schedule.student_vip_id = :val1 and proposed_schedule.semester= :val2', \
        {'val1': current_user.vip_id, 'val2': session['term']})
    if request.method == 'POST':
        total_hours = request.form.get('total_hours')
        if total_hours == '0':
            flash('Error: You cannot submit a schedule with zero classes added.', 'danger')
        elif request.form['btn'] == 'Delete':
            course_crn = request.form.get('remove_course_crn')
            course = proposedSchedule.query.filter_by(student_vip_id=current_user.vip_id, course_crn=course_crn, semester=session['term']).delete()
            db.session.commit()
            flash('Class has been deleted.', 'dark')
        else:
            flash('Your schedule has been submitted to your advisor for feedback!', 'dark')
            semester = session['term']
            new_schedule = submittedSchedules(student_vip_id = current_user.vip_id, advisor_vip_id = current_user.advisor_id, semester = semester, status = 'Needs Review')
            db.session.add(new_schedule)
            db.session.commit()
        return redirect(url_for('review_schedule_student'))
    return render_template('review-schedule.html', classes=list(classes), hours=hours.first(), semester=session['term'])


@app.route('/advisor-info', methods=['GET', 'POST'])
@login_required
def advisor_info():
    advisor = db.session.execute('SELECT * FROM advisor WHERE vip_id = :val', {'val': current_user.advisor_id})
    return render_template('advisor-info.html', advisor=advisor)




############# Advisor pages ##############

@app.route('/approve-schedules', methods=['GET', 'POST'])
@login_required
def approve_schedules():
    student = Student.query.filter_by(vip_id=current_user.vip_id).first()
    advisor = Advisor.query.filter_by(vip_id=current_user.vip_id).first()
    if advisor is None:
        return redirect(url_for('build_schedule'))
    schedules = db.session.execute("select student.name, substr(submitted_schedules.submit_datetime, 1, pos1-1) as submitted_date, \
        submitted_schedules.student_vip_id, submitted_schedules.semester, submitted_schedules.status from (select *, instr(submit_datetime, ' ') as pos1 \
        from submitted_schedules) as submitted_schedules left join student on submitted_schedules.student_vip_id = student.vip_id \
        where advisor_vip_id = :val1", {"val1": current_user.vip_id})
    if request.method == 'POST':
        session['student_vip_id'] = request.form.get('view_schedule_vip_id')
        session['semester'] = request.form.get('view_schedule_semester')
        session['student_name'] = request.form.get('view_schedule_name')
        return redirect(url_for('review_schedule_advisor'))
    return render_template('approve-schedules.html', schedules=schedules)

@app.route('/review-schedule-advisor-view', methods=['GET', 'POST'])
@login_required
def review_schedule_advisor():
    student_name = session['student_name']
    semester = session['semester']
    classes = db.session.execute('SELECT courses.* FROM proposed_schedule \
        left JOIN courses on proposed_schedule.course_crn = courses.crn \
        where proposed_schedule.student_vip_id = :val1 and proposed_schedule.semester= :val2', \
        {'val1': session['student_vip_id'], 'val2': session['semester']})
    hours = db.session.execute('SELECT (case when sum(courses.credit_hours) > 0 then sum(courses.credit_hours) else 0 end) \
        as "sum"  FROM proposed_schedule \
        left JOIN courses on proposed_schedule.course_crn = courses.crn \
        where proposed_schedule.student_vip_id = :val1 and proposed_schedule.semester= :val2', \
        {'val1': session['student_vip_id'], 'val2': session['semester']})
    return render_template('review-schedule-advisor-view.html', classes=list(classes), hours=hours.first(), student_name=session['student_name'], semester = semester)
