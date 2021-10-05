from flask import Flask
import pandas as pandas


app = Flask(__name__)

def alimente_caisse(date,amount,type):
    if type == 'PRET':
        pass
    elif type == 'INVEST':
        pass
    elif type == 'SALE':
        pass
    else :
        print('PLease specify the origin of the input !')

def add_invest(**kwargs):
    pass
