
from twilio.rest import Client

twilio_number = "" 
twilio_account = ""
twilio_token = ""

# Sends an SMS to user's number with update
def notify_user(phone, update):

    # Credentials
    account = twilio_account
    token = twilio_token
    client = Client(account, token)
    
    # Message
    client.messages.create(
        to = phone,
        from_ = twilio_number,
        body = update
    )
