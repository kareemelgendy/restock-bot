import os
from twilio.rest import Client


# Sends SMS using Twilio API
def notify_user(phone, msg):
    try:
        client = Client(os.environ['TWILIO_ACCOUNT_SID'],
                        os.environ['TWILIO_AUTH_TOKEN'])

        client.messages.create(
            to=phone,
            from_=os.environ['TWILIO_NUM'],
            body=msg
        )
        print('\n\U0001F4F2 SMS successfully sent!')

    except KeyError:
        print('\n\U0001F6D1 Failed to notify user - invalid Twilio API credentials')
