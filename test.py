import unittest
from main import *
from test_login_page import *
from test_listing_page import *
import requests

class SharetribeUploaderTests(unittest.TestCase):
    
    def test_list_item(self):
        book_item = {
            'title': 'Men Explain Things To Me',
            'price': '5',
            'delivery': 'ship',
            'description': 'This is a book about how men always explain things to women...'
        }
        response = list_item()
        self.assertIsNotNone(response)
        self.assertTrue(response)

    def test_login(self):
        session = login()
        print("cookie = " + session.cookies['_st_com_session']);
        self.assertTrue(session.cookies['_st_com_session'], 'No cookie returned, login failed.')
        self.assertEqual(len(session.cookies['_st_com_session']), 32, 'Cookie value not 32 characters long')
    
    def test_connection(self):
        self.assertIsNotNone(fetch_site(), 'Sharetribe site response is null')

    def test_get_login_auth_token(self):
        content = get_test_login_page()
        extracted_tokens = get_login_auth_token(content[1])
        self.assertEqual(len(extracted_tokens), 1, 'Multiple tokens extracted from login page.');
        print("login_auth_token = " + ','.join(map(str, extracted_tokens)));
        self.assertEqual(extracted_tokens, [content[0]], 'Authenticity token incorrect')

    def test_get_listing_auth_token(self):
        content = get_test_listing_page();
        extracted_tokens = get_listing_auth_token(content[1]);
        self.assertEqual(len(extracted_tokens), 1, 'Multiple tokens extracted from listing page.');
        print("listing_page_token = " + ','.join(map(str, extracted_tokens)));
        self.assertEqual(extracted_tokens, [content[0]], 'Incorrect authenticity token')

    def test_build_list_post_url(self):
        cat     = '1234'
        subcat  = 'abcd'
        lshape  = 'wxyz'
        url = build_list_post_url(cat, subcat, lshape)
        self.assertEqual(url, 'https://fairmondo.uk.sharetribe.com/en/listings/new?category=' + cat + '&subcategory=' + subcat + '&listing_shape=' + lshape, 'post listing url not correctly formed')


    

