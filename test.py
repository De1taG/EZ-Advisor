from ezadvisor import app
import unittest
from flask_testing import TestCase

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

    #Ensure the main page required login
    def test_main_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/get-started', follow_redirects= True)
        self.assertTrue(b'Please log in to access this page.' in response.data)

    #Ensure that getstarted redirects to choose classes
    def test_get_started(self):
        tester = app.test_client(self)
        response = tester.post('/index', data=dict(username= '34908943', password='FisherPassword'), follow_redirects=True)
        self.assertIn(b'schedule', response.data)

    #Ensure that the name of the of the user logged in is correct
    # def test_id_correct(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/index', data=dict(username= '34908943', password='FisherPassword'), follow_redirects=True)
        

    #Ensure that the logged in user is active
    # def test_user_loaded(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/index', data=dict(username= '34908943', password='FisherPassword'), follow_redirects=True)
    #     

    def tearDown(self):
        app.config['TESTING'] = False
        app.config['WTF_CSRF_ENABLED'] = True
    

if __name__ == '__main__':
    unittest.main()