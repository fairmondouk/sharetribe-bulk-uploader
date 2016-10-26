#!/usr/local/bin/python3
import requests
from bs4 import BeautifulSoup as bs

def fetch_site():
    ST_URL = 'https://fairmondo-uk.sharetribe.com/en/listings/new?category=119444&subcategory=122284&listing_shape=36341'
    r = requests.get(ST_URL)
    return r

# raw response contains multiple auth_tokens for differnt login attempts
# this function extracts token for normal login.
def get_auth_token(raw_resp, formName):
    soup = bs(raw_resp, 'lxml')
    form = soup.find("div", {"class": formName});
    token = [n['value'] for n in form.find_all('input')
                if n.get('name') == 'authenticity_token']
    return token 

def get_listing_auth_token(page):
    return get_auth_token(page, "js-form-fields");

def get_login_auth_token(page):
    return get_auth_token(page, "login-form");

def set_session_cookie(s):
    LOGIN_URL = 'https://fairmondo-uk.sharetribe.com/en/login'
    SESSION_URL = 'https://fairmondo-uk.sharetribe.com/en/sessions'
    
    resp = s.get(LOGIN_URL)
    auth_token = get_auth_token(resp.text, "login-form") 
    
    payload = {
        'utf8': '✓',
        'person[login]': 'jack@fairmondo.uk',
        'person[password]': 'Proth-13',
        'authenticity_token': auth_token
    }
    
    s.post(SESSION_URL, data=payload);
    return s;

def build_list_post_url(cat, subcat, lshape):
    LISTING_URL = 'https://fairmondo-uk.sharetribe.com/en/listings/new'
    return LISTING_URL + '?category=' + cat + '&subcategory=' + subcat + '&listing_shape=' + lshape

def login():
    s = requests.session()
    set_session_cookie(s);
    return s;

# Build the form-data encoded data for posting a listing.
def build_listing_object(authToken):
    listing = {
        'utf8': '✓',
        'authenticity-token': authToken,
        'listing[title]': 'The lean startup',
        'listing[price]': '14.99',
        'listing[currency]': 'GBP',
        'listing[unit]': '{"type":"custom","name_tr_key":"2a963aef-7acd-475d-bc47-aca89e854958","kind":"quantity","selector_tr_key":"a0533f26-872d-42fe-b232-0274dee3b83a","quantity_selector":"number"}',
        'listing[delivery_methods][]' : 'shipping',
        'listing[currency]': 'GBP',
        'listing[shipping_price]': '2.00',
        'listing[currency]': 'GBP',
        'listing[shipping_price_additional]': '0.00',
        'listing[description]': "The Lean Startup isn't just about how to create a more successful entrepreneurial business... it's about what we can learn from those businesses to improve virtually everything we do. I imagine Lean Startup principles applied to government programs, to healthcare, and to solving the world's great problems. It's ultimately an answer to the question 'How can we learn more quickly what works, and discard what doesn't?  ISBN: 978-0-670-92160-7",
        'custom_fields[21879]': '1',
        'listing[origin]': 'Keighley, UK',
        'listing[origin_loc_attributes][address]': 'Keighley, UK',
        'listing[origin_loc_attributes][google_address]': 'Keighley, UK',
        'listing[origin_loc_attributes][latitude]': '53.8678',
        'listing[origin_loc_attribures][longitude]': '-1.91236',
        'listing[category_id]': '122284',
        'listing[listing_shape_id]': '36341',
        'listing_images[][id]': '',
        'listing_images[][id]': '',
        'listing_images[][id]': '',
    }
    return listing

def list_item():
    BOOK_CAT_NO = '119444'   
    BOOK_SUBCAT_NO = '122284'
    SALE_LISTING_SHAPE_NO = '36341'
    listingUrl = build_list_post_url(BOOK_CAT_NO, BOOK_SUBCAT_NO, SALE_LISTING_SHAPE_NO)
    
    session = login();
    listingPage = session.get(listingUrl);
    listingAuthToken = get_listing_auth_token(listingPage.text);
    item = build_listing_object(listingAuthToken);

    POST_LISTING_URL = 'https://fairmondo-uk.sharetribe.com/en/listings';
    # post multipart form for listing.
    post_res = session.post(POST_LISTING_URL, files=item)
    #item = '';
    print(post_res);
    return



