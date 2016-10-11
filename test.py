import unittest
from main import *

class SharetribeUploaderTests(unittest.TestCase):
    
    def test_list_item(self):
        book_item = {
            'title': 'Men Explain Things To Me',
            'price': '5',
            'delivery': 'ship',
            'description': 'This is a book about how men always explain things to women...'
        }
        response = list_item(book_item)
        self.assertIsNotNone(response)
        self.assertTrue(response)

    def test_login(self):
        session_cookie = get_session_cookie()
        self.assertEqual(session_cookie['name'], '_st_com_session', 'Cookie name not correct')
        self.assertEqual(len(session_cookie['value']), 32, 'Cookie value not 32 characters long')
    
    def test_connection(self):
        self.assertIsNotNone(fetch_site(), 'Sharetribe site response is null')

    def test_get_auth_token(self):
        auth_token = "abcd"
        html_page = "<html><h1>WEBPAGE</h1><form><input name='authenticity_token' value='" + auth_token +  "'</form></html>"
        self.assertEqual(get_auth_token(html_page), [auth_token], 'Form not extracted correctly')

    

