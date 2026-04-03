import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

sid = os.getenv("TWILIO_ACCOUNT_SID")
token = os.getenv("TWILIO_AUTH_TOKEN")
from_num = os.getenv("TWILIO_FROM_NUMBER")
base_url = os.getenv("BASE_URL")

# Test destination number (Change this to the user's number or a verified one)
test_to = "+919657795009" # Verified number in Twilio console

def main():
    if not sid or not token or not from_num:
        print("[-] MISSING TWILIO CREDENTIALS in .env")
        return

    print(f"[*] SID: {sid[:5]}...")
    print(f"[*] FROM: {from_num}")
    print(f"[*] BASE_URL: {base_url}")
    print(f"[*] TO: {test_to}")

    client = Client(sid, token)
    twiml_url = f"{base_url.rstrip('/')}/api/voice/twiml"
    
    try:
        print(f"[*] Attempting call via TwiML: {twiml_url}")
        call = client.calls.create(
            url=twiml_url,
            to=test_to,
            from_=from_num
        )
        print(f"[+] Call triggered successfully! SID: {call.sid}")
        print(f"[+] Status: {call.status}")
    except Exception as e:
        print(f"[!] FAILED TO CREATE CALL")
        print(f"[!] Error: {str(e)}")
        if "21219" in str(e):
            print("[!] DIAGNOSIS: Twilio Trial Account detected. You MUST verify the destination number in Twilio Console (Verified Caller IDs).")
        elif "21211" in str(e):
            print("[!] DIAGNOSIS: Invalid 'To' number format.")
        elif "20003" in str(e):
            print("[!] DIAGNOSIS: Permission Denied. Check your Twilio account permissions.")

if __name__ == "__main__":
    main()
