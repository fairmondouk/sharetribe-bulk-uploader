#!/usr/local/bin/python3
import requests
from bs4 import BeautifulSoup as bs

def fetch_site():
    ST_URL = 'https://fairmondo-uk.sharetribe.com/en/listings/new?category=119444&subcategory=122284&listing_shape=36341'
    r = requests.get(ST_URL)
    return r

def get_auth_token(raw_resp):
    soup = bs(raw_resp, 'lxml')
    token = [n['value'] for n in soup.find_all('input')
                if n['name'] == 'authenticity_token']
    return token 

def get_session_cookie():
    LOGIN_URL = 'https://fairmondo-uk.sharetribe.com/en/login'
    SESSION_URL = 'https://fairmondo-uk.sharetribe.com/en/sessions'
    with requests.session() as s:
        resp = s.get(LOGIN_URL)
        print(resp.text)
        
        auth_token = get_auth_token(resp.text) 
        '''
        payload = {
            'utf8': '✓',
            'person[login]': 'jack@fairmondo.uk',
            'person[password]': 'Proth-13',
            'authenticity_token': auth_token
        }
        
        post_response = s.post(SESSION_URL, data=payload);
        print(post_response.cookies);
        '''
    return {'name':'b', 'value': 'sd'}

get_session_cookie();
