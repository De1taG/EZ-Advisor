from ezadvisor import app
import unittest

class EZAdvisorTest(unittest.TestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/index', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    #Ensure that the index page loads correctly
    def test_index_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/index', content_type='html/text')
        self.assertTrue(b'Password' in response.data)
    
    #Ensure login behaves correctly given the correct credentials
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post('/index', data=dict(username='23404460', password='ReedPassword'), follow_redirects=True)
        self.assertIn(b'WELCOME', response.data)
    
    #Ensure login behaves correctly given incorrect credentials

    
    #Ensure login behaves correctly given the correct credentials
    

if __name__ == '__main__':
    unittest.main()