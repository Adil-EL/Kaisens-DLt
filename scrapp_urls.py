import requests
import urllib
import json
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
from collections import OrderedDict
import time
from bs4 import BeautifulSoup

def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def scrape_google(subject,social_media):
    """
        Search on google the facebook [Social media] posts related to the death of 
    Jaques Chirac [Subject] 

    inputs :

    subject : the subject you are intersted in (the death of Jacques chirac for example)
    social_media : sting, the name of the social media you want to find information in
    FACEBOOK for exmample.
    

    Output:
    This function returns a list of urls dealing with subject and save it as a json file 
    """

    query = subject + ' ' + social_media
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links




def get_bs(url):
    """
    Makes a GET requests using the given Session object
    and returns a BeautifulSoup object.
    
    """
    r = None
    while True:
        r = requests.get(url)
        time.sleep(3)
        if r.ok:
            break
    return BeautifulSoup(r.text, 'html.parser')


def extract_comments(session, base_url, post_bs, post_url):
    """
    Extracts all coments from post
    """
    comments = list()
    show_more_url = post_bs.find('a', href=re.compile('/story\.php\?story'))['href']
    first_comment_page = True

    logging.info('Scraping comments from {}'.format(post_url))
    while True:

        logging.info('[!] Scraping comments.')
        time.sleep(3)
        if first_comment_page:
            first_comment_page = False
        else:
            post_bs = get_bs(session, base_url+show_more_url)
            time.sleep(3)
        
        try:
            comments_elements = post_bs.find('div', id=re.compile('composer')).next_sibling\
                .find_all('div', id=re.compile('^\d+'))
        except Exception:
            pass

        if len(comments_elements) != 0:
            logging.info('[!] There are comments.')
        else:
            break
        
        for comment in comments_elements:
            comment_data = OrderedDict()
            comment_data['text'] = list()
            try:
                comment_strings = comment.find('h3').next_sibling.strings
                for string in comment_strings:
                    comment_data['text'].append(string)
            except Exception:
                pass
            
            try:
                media = comment.find('h3').next_sibling.next_sibling.children
                if media is not None:
                    for element in media:
                        comment_data['media_url'] = element['src']
                else:
                    comment_data['media_url'] = ''
            except Exception:
                pass
            
            comment_data['profile_name'] = comment.find('h3').a.string
            comment_data['profile_url'] = comment.find('h3').a['href'].split('?')[0]
            comments.append(dict(comment_data))
        
        show_more_url = post_bs.find('a', href=re.compile('/story\.php\?story'))
        if 'View more' in show_more_url.text:
            logging.info('[!] More comments.')
            show_more_url = show_more_url['href']
        else:
            break
    
    return comments


def scrape_post( url):
    """
    Goes to post URL and extracts post data.
    This functions extracts relevant information from a social media post.
    
    Input :
    url : the url of a social media post related to a subject
    extract the content and put it in a dictionnary

    output :
    returns a python dictionnary of relevant content related to a subject, the post url,
    the text in the post, the media (images, videos,etc) and all the comments (a nested 
    dictionnary with comment's specific keys (attributes))
    
    """
    post_data = OrderedDict()

    post_bs = get_bs(url)
    time.sleep(2)

    # Here we populate the OrderedDict object
    post_data['url'] = url

    try:
        post_text_element = post_bs.find('div', id='jsc_c_1w').div
        string_groups = [p.strings for p in post_text_element.find_all('p')]
        strings = [repr(string) for group in string_groups for string in group]
        post_data['text'] = strings
    except Exception:
        post_data['text'] = ['test text 1','test text 2']
    
    try:
        post_data['media_url'] = post_bs.find('div', id='jsc_c_1w').find('a')['href']
    except Exception:
        post_data['media_url'] = 'www.test-scrapping.com'
    

    try:
        post_data['comments'] = extract_comments(session, base_url, post_bs, post_url)
    except Exception:
        post_data['comments'] = []
    
    return dict(post_data)



#------------------------------ Scrapped data good practices----------------
""" To be implemented in later updates """

def save_json_urls(urls_list):
    ''' 
    This function saves on the desk the elements of a list as a json file 
    '''
    with open('app.json', 'w') as f:
        json.dump(urls_list, f)

def load_json_urls():
    '''
    returns a python list containing the urls scrapped from google

    '''
    pass






