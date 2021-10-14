from pymongo import MongoClient
import pymongo

def add_content_db(content,db):
    """
    The aim of this function is to add a scrapped post content to a MongoDB database
    """
    try :
        db.content.insert_one(content)
        print('content added succesfully')
    
    except:
        print('DB error message')
    

#--------------------------------- Costumized interaction methods may be implemented in later versions-------------

def custum_func_1(_):
    pass

def custum_func_2(_):
    pass