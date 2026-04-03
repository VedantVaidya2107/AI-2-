import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
from_number = os.environ.get("TWILIO_FROM_NUMBER")
to_number = "+919182916194" # Testing with the 'dfg' number from dashboard

print(f"Testing Twilio Call...")
print(f"SID: {account_sid}")
print(f"From: {from_number}")
print(f"To: {to_number}")

try:
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        from_=from_number,
        to=to_number,
        url="http://demo.twilio.com/docs/voice.xml" # Use a standard Twilio demo XML
    )
    print(f"SUCCESS! Call SID: {call.sid}")
except Exception as e:
    print(f"FAILED: {e}")
