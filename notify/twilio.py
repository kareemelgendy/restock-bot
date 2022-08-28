from twilio.rest import Client
import os


def notify_user(phone, msg):
    try:
        client = Client(os.environ['TWILIO_ACCOUNT'],
                        os.environ['TWILIO_TOKEN'])

        client.messages.create(
            to=phone,
            from_=os.environ['TWILIO_NUM'],
            body=msg
        )

    except:
        print('Failed to notify user - Twilio API credentials invalid or not found.')
