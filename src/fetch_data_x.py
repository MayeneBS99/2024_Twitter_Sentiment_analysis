# import librairies

from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint

MINIMUM_TWEETS = 10
QUERY = 'france'

# login credentials
config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

# authenticate to X.com
client = Client(language = 'fr-FR')
client.login(auth_info_1= username, auth_info_2= email, password=password)
client.save_cookies('cookies.json')