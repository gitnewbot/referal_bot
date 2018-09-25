import configparser
import os

import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

config = configparser.ConfigParser()
config.read('config.ini')
if os.path.exists('my_config.ini'):
    config.read('my_config.ini')

               
engine = create_engine(config['APPLICATION']['DB_CONNECT'])   
Session = sessionmaker(bind=engine)    
