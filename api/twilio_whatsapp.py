import os
from twilio.rest import Client
from dotenv import load_dotenv


# Load environment variables from the .env file (if present)
load_dotenv('env/dev.env')


import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        kwargs['ssl_context'] = ctx
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)


account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_KEY')
twilio_number=os.getenv('TWILIO_NUMBER')
receivers_number=os.getenv('PHONE_NUMBER')


session = requests.Session()
session.mount('https://', SSLAdapter())

client = Client(account_sid, auth_token, http_client=session)
def send_to_phone(msg:str,phone_num:str):
    if(phone_num==None or phone_num==""):
        phone_num=receivers_number
    message = client.messages.create(
        body=f'{msg}',
        from_=f'whatsapp:{twilio_number}',  # This is Twilio's sandbox number
        to=f'whatsapp:{phone_num}'  # Replace with the recipient's phone number
    )

    print(message.sid)
    return message.sid
