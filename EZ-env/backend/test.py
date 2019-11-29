from ezadvisor import app, db
from ezadvisor.data import Student
import unittest
from flask_testing import TestCase
from flask_login import current_user

class EZAdvisorTest(unittest.TestCase):

    # Unit tests
    # Requirements testing
    # Coverage
    # Test cases

    # Command for coverage: pytest --cov=ezadvisor test.py  --cov-report=html
    
    #Flask comes with a test client, which allows our tests
    #to mimick actual client requests. So esentially we are 
    #setting up a simulated, isolated app for testing requests
    #and responses.

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        #making a connection to primary database is safe for now because Test Suite is only reading
        #from it.
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
        db.create_all()

    # Ensure that Flask app loads correctly with a successful response
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/index', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    #Ensure that index.html loads
    def test_index_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/index', content_type='html/text')
        self.assertTrue(b'Password' in response.data)
    
    #Ensure login is successfuly given the correct username and password
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post('/index', data=dict(username='23404460', password='ReedPassword'), follow_redirects=True)
        self.assertIn(b'Logout', response.data)
    
    #Ensure login works correctly given incorrect username and password

    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post('/index', data=dict(username= 'wrong_name', password='wrong_password'), follow_redirects=True)
        self.assertIn(b'Login', response.data)
    
    #Ensure logout behaves correctly
    def test_logout(self):
        tester = app.test_client(self)
        response = tester.get('/logout', follow_redirects= True)
        self.assertIn(b'Password', response.data)

    #Ensure the main page requires login
    def test_main_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/get-started', follow_redirects= True)
        self.assertTrue(b'Please log in to access this page.' in response.data)

    #Ensure that students are directed to choose classes
    def test_build_schedules(self):
        tester = app.test_client(self)
        response = tester.post('/index', data=dict(username= '34908943', password='FisherPassword'), follow_redirects=True)
        self.assertIn(b'schedule', response.data)

    #Ensure that advisors are directed to approve schedules
    def test_approve_schedules(self):
        tester = app.test_client(self)
        response = tester.post('/index', data=dict(username= '20424585', password='DiemerPassword'), follow_redirects=True)
        self.assertIn(b'approve', response.data)

    #Ensure that the correct advisor is logged in and active
    def test_advisor_name_active(self):
        tester = app.test_client(self)
        with tester:
            response = tester.post('/index', data=dict(username= '20424585', password='DiemerPassword'), follow_redirects=True)
            self.assertTrue(current_user.name == 'Nick Diemer')
            self.assertTrue(current_user.is_active())

    #Ensure that the correct student is logged in and active
    def test_student_name_active(self):
        tester = app.test_client(self)
        with tester:
            response = tester.post('/index', data=dict(username= '34908943', password='FisherPassword'), follow_redirects=True)
            self.assertTrue(current_user.name == 'Garrett Fisher')
            self.assertTrue(current_user.is_active())

    #Ensure that the right major and advisor corresponds to the logged in student
    def test_student_attributes(self):
        tester = app.test_client(self)
        with tester:
            response = tester.post('/index', data=dict(username= '34908943', password='FisherPassword'), follow_redirects=True)
            self.assertTrue(current_user.email == 'gfisher@uscupstate.edu')
            self.assertTrue(current_user.major_title == 'Computer Science')
            self.assertTrue(current_user.advisor_id == 20424585)

    #Ensure that the right attributes corresponds to the logged in advisor
    def test_advisor_actributes(self):
        tester = app.test_client(self)
        with tester:
            response = tester.post('/index', data=dict(username= '20424585', password='DiemerPassword'), follow_redirects=True)
            self.assertTrue(current_user.job == 'Professor')
            self.assertTrue(current_user.department == 'Computer Science')
            self.assertTrue(current_user.phone == '(864) 123-4567')
            self.assertTrue(current_user.office == 'Hodge 201')
            self.assertTrue(current_user.email == 'ndiemer@uscupstate.edu')

    #Ensure that the system is not keeping track of the wrong logged in users
    def test_user_name_wrong(self):
        tester = app.test_client(self)
        with tester:
            response = tester.post('/index', data=dict(username= '34908943', password='FisherPassword'), follow_redirects=True)
            self.assertFalse(current_user.name == 'Wrong_Person')

    def tearDown(self):
        app.config['TESTING'] = False
        app.config['WTF_CSRF_ENABLED'] = True
    

if __name__ == '__main__':
    unittest.main()