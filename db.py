from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert, text,update,delete, create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
import os

def check_if_database_exists(database_url):
    
    if not database_exists(database_url):
        create_database(database_url)

        Base = declarative_base()



        

db=SQLAlchemy()





