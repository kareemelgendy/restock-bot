
#from twilio.rest import Client
from twilio.rest import Client
from twilio_cred import *

def notify_user(phone, update):

    account = twilio_account
    token = twilio_token
    client = Client(account, token)

    client.messages.create(
        to = phone,
        from_ = twilio_number,
        body = update
    )
