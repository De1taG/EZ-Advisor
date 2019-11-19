from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///EZ-Advisor.db'
db = SQLAlchemy(app)

required = db.Table('required',
    db.Column('major', db.String(40), db.ForeignKey('major.title')),
    db.Column('requirement_area', db.String(30)),
    db.Column('sub_area', db.String(30)),
    db.Column('course_id', db.String(10), db.ForeignKey('catalog.course_id')))

completedCourses = db.Table('completedCourses',
    db.Column('student_id', db.Integer, db.ForeignKey('student.vip_id')),
    db.Column('course_id', db.String(10), db.ForeignKey('catalog.course_id')),
    db.Column('grade', db.String(3)))

registered = db.Table('registerd',
    db.Column('student_id', db.Integer, db.ForeignKey('student.vip_id')),
    db.Column('course_id', db.String(10), db.ForeignKey('courses.course_id')),
    db.Column('submit', db.Date))

class Advisor(db.Model):
    vip_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    password = db.Column(db.String(25))
    email = db.Column(db.String(50))
    building = db.Column(db.String(50))
    student = db.relationship('Student', backref='advisor', lazy='joined')

class Student(db.Model):
    vip_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    password = db.Column(db.String(25))
    email = db.Column(db.String(50))
    major_title = db.Column(db.String(50), db.ForeignKey('major.title'))
    advisor_id = db.Column(db.Integer, db.ForeignKey('advisor.vip_id'))
    completed_Course = db.relationship('Catalog', secondary=completedCourses, backref=db.backref('completed', lazy='dynamic'))
    registered = db.relationship('Courses', secondary=registered, backref=db.backref('registered', lazy='dynamic'))

class Major(db.Model):
    title = db.Column(db.String(40), primary_key=True)
    description = db.Column(db.String(150))
    student = db.relationship('Student', backref='major')

class Catalog(db.Model):
    course_id = db.Column(db.String(10), primary_key=True)
    course_title = db.Column(db.String(40))
    course_desc = db.Column(db.String(250))
    prereq = db.Column(db.String(100))
    credit_hours = db.Column(db.Integer)
    major = db.relationship('Major', secondary=required, backref=db.backref('required', lazy='dynamic'))
    course_offered = db.relationship('Courses', backref='course', lazy='joined')

class Courses(db.Model):
    course_id = db.Column(db.String(10), db.ForeignKey('catalog.course_id'), primary_key=True)
    section_num = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.String(10), db.ForeignKey('semester.semester'), primary_key=True)
    day = db.Column(db.String(5))
    start_time_MWF = db.Column(db.String(10))
    end_time_MWF = db.Column(db.String(10))
    start_time_TTh = db.Column(db.String(10))
    end_time_TTh = db.Column(db.String(10))

class Semester(db.Model):
    semester = db.Column(db.String(10), primary_key=True)
    course_present = db.relationship('Courses', backref='semester_taken')

