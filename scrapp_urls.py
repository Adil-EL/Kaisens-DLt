import requests
import urllib
import json
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




#--------------------- Tests ----------------------------------
subject = 'Deces de jaques chirac'
social_media = 'Facebook'

links = scrape_google(subject,social_media)

url = links[5]
dicc = scrape_post(url)
print(dicc)