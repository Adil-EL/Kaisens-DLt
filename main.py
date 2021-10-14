
import pymongo
from pymongo import MongoClient

from scrapp_urls import scrape_google, scrape_post


links = scrape_google('kaisens data', 'facebook')
url = links[5]

res = scrape_post(url)
print(res)









# #--------------------- Helper functions--------------------

# def urls_collector(base_url, subject,social_media, max_posts):
#     ''' 
#     Search on google the facebook [Social media] posts related to the death of 
#     Jaques Chirac [Subject] 

#     inputs :

#     base_url : the seach engine you want to use (Google for example)
#     subject : the subject you are intersted in (the death of Jacques chirac for example)
#     social_media : sting, the name of the social media you want to find information in
#     FACEBOOK for exmample.
#     max_posts : the maximum number of posts you want to deal with.

#     Output:
#     This function returns a list of urls dealing with subject and save it as a json file 


#     '''
#     url = base_url + subject + ' ' + social_media
#     reqs = requests.get(url)
#     soup = BeautifulSoup(reqs.text, 'html.parser')
 
#     urls = []
#     for link in soup.find_all('a'):
#         url = link.get('href')
#         print(url)
#         urls.append(url)
    

#     return urls

# def save_json_urls(urls_list):
#     ''' 
#     This function saves on the desk the elements of a list as a json file 
#     '''
#     with open('app.json', 'w') as f:
#         json.dump(urls_list, f)

# def load_json_urls():
#     '''
#     returns a python list containing the urls scrapped from google

#     '''
#     pass

# def save_to_MDB(content,db):
#     '''
#      This function formats and saves a python dictionnary of content to a dedicated  
#      MongoDB database, this function create a new document in the database each time
#      the content of a publication is scrapped

#      for a purpose of simpliciry the default url is used for the database (localhost:27017)

#     '''
#     db.content.insert_one(content)



# #--------------------------- Main function -------------------------------------------

# def social_media_events_scrapper(base_url,session,subject,social_media,db = db):
#     '''
#     This fucntion agregate the helper functions to produce the needed output

#     '''
#     urls_list = urls_collector(base_url = base_url, subject = subject,social_media =social_media, max_posts = 20)

#     for url in urls_list:
#         content = content_scrapping(url)
#         save_to_MDB(content = content,db = db)



# if __name__ == "__main__":

#     client = MongoClient()
#     db=client.posts
#     BASE_URL = 'https://google.com/search?q='
#     session = requests.session()
#     SUBJECT = 'Deces de jaques chirac'
#     SOCIAL_MEDIA = 'Facebook'
#     social_media_events_scrapper(base_url = BASE_URL,subject = SUBJECT,social_media = SOCIAL_MEDIA, db = db)

