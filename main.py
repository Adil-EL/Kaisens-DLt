import requests
import json
import time
import collections
import re
from bs4 import BeautifulSoup



#--------------------- Helper functions--------------------

def Links_Collector(base_url, subject,social_media, max_posts):
    ''' 
    Search on google the facebook [Social media] posts related to the death of 
    Jaques Chirac [Subject] 

    inputs :

    base_url : the seach engine you want to use (Google for example)
    subject : the subject you are intersted in (the death of Jacques chirac for example)
    social_media : sting, the name of the social media you want to find information in
    FACEBOOK for exmample.
    max_posts : the maximum number of posts you want to deal with.

    Output:
    This function returns a list of urls dealing with subject and save it as a json file 


    '''
    url = base_url + subject + ' ' + social_media
    url = "https://www.geeksforgeeks.org/"
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
 
    urls = []
    for link in soup.find_all('a'):
        print(link.get('href'))
    

    pass

def save_json_urls(urls_list):
    ''' 
    This function saves on the desk the elements of a list as a json file 
    '''
    pass

def load_json_urls():
    '''
    returns a python list containing the urls scrapped from google

    '''
    pass

def content_scrapping(url):
    ''' 
    This functions extracts relevent information from a social media post.
    
    Input :
    url : the url of a social media post related to a subject
    extract the content and put it in a dictionnary

    output :
    returns a python dictionnary of relevent content related to a subject
    '''
    pass

def save_to_MDB(content):
    '''
     This function formats and saves a python dictionnary of content to a dedicated  
     MongoDB database
    '''
    pass



#--------------------------- Main function -------------------------------------------

def social_media_events_scrapper(base_url,session,subject,social_media):
    '''
    This fucntion agregate the helper functions to produce the needed output

    '''

    print('The BluePrint is working as expected')
    
    Links_Collector(base_url = base_url, subject = subject,social_media =social_media, max_posts = 20)


if __name__ == "__main__":

    BASE_URL = 'https://google.com/search?q='
    session = requests.session()
    SUBJECT = 'Deces de jaques chirac'
    SOCIAL_MEDIA = 'Facebook'

    social_media_events_scrapper(base_url = BASE_URL, session = session,subject = SUBJECT,social_media = SOCIAL_MEDIA)


















# app = Flask(__name__)

# def alimente_caisse(date,amount,type):
#     if type == 'PRET':
#         pass
#     elif type == 'INVEST':
#         pass
#     elif type == 'SAIL':
#         pass
#     else :
#         print('PLease specify the origin of the input !')

# def add_invest(**kwargs):
#     pass

