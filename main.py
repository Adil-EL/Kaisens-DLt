
from pymongo import MongoClient

from scrapp_urls import scrape_google, scrape_post

from MongoDB_management import add_content_db


# #--------------------------- Main function -------------------------------------------

def social_media_events_scrapper(subject,social_media,db):
    """
    This fucntion agregate the helper functions to produce the needed output

    """
    urls = scrape_google(subject, social_media)
    for url in urls:
        content = scrape_post(url)
        add_content_db(content = content,db = db)



if __name__ == "__main__":

    client = MongoClient()
    db=client.posts
    SUBJECT = 'Deces de jaques chirac'
    SOCIAL_MEDIA = 'Facebook'
    social_media_events_scrapper(subject = SUBJECT,social_media = SOCIAL_MEDIA, db = db)