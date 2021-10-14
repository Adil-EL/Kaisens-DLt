import requests
import urllib
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


def scrape_google(query):

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
    """Makes a GET requests using the given Session object
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
    """Extracts all coments from post
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
    """Goes to post URL and extracts post data.
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
    

    # try:
    #     post_data['comments'] = extract_comments(session, base_url, post_bs, post_url)
    # except Exception:
    #     post_data['comments'] = []
    
    return dict(post_data)


links = scrape_google(query = 'mort de jaques chirac facebook')
url = links[5]
print(scrape_post( url))










# import requests
# from bs4 import BeautifulSoup

# base_url = 'https://google.com/search?q='

# subject = 'mort de jacques chirac'
# social_media = 'facebook'

# url = base_url + subject + ' ' + social_media
# url = 'https://google.com/search?q=<Query>'
# reqs = requests.get(url)
# soup = BeautifulSoup(reqs.text, 'html.parser')

# urls = []
# for link in soup.find_all('a'):
#     url = link.get('href')
#     print(url)
#     urls.append(url)



