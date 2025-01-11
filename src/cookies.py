from twikit import Client
import asyncio
from configparser import ConfigParser


config = ConfigParser()
config.read('C:/Users/mayen/PROJET_IEF2I/src/config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

async def login_and_save_cookies():
    client = Client(language='en-EN')
    await client.login(auth_info_1=username, auth_info_2=email, password=password)
    client.save_cookies(r'C:\Users\mayen\PROJET_IEF2I\src\cookies.json')
    print("Cookies saved successfully.")

if __name__ == "__main__":
    asyncio.run(login_and_save_cookies())
