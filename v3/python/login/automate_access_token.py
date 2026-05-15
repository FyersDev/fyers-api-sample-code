import os
import pyotp
import requests
from urllib.parse import parse_qs, urlparse
from fyers_apiv3 import fyersModel
from dotenv import load_dotenv, set_key

# Load environment variables from .simple.env in the parent directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)

def access_token_generator():
    # Fetch credentials from environment
    client_id = os.getenv("client_id")
    app_id = client_id.split('-')[0]
    app_type = client_id.split('-')[1] if '-' in client_id else "200"
    fy_id = os.getenv("user_id", "").upper()
    totp_key = os.getenv("totp_key")
    pin = f"{os.getenv('pin1')}{os.getenv('pin2')}{os.getenv('pin3')}{os.getenv('pin4')}"
    redirect_uri = os.getenv("redirect_uri")
    secret_key = os.getenv("secret_key")

    req = requests.Session()
    BASE_2 = "https://api-t2.fyers.in/vagator/v2"
    BASE_3 = "https://api-t1.fyers.in/api/v3"
    
    try:
        # 1. Send Login OTP
        res = req.post(f"{BASE_2}/send_login_otp", json={"fy_id": fy_id, "app_id": "2"}).json()
        
        # 2. Verify TOTP
        res = req.post(f"{BASE_2}/verify_otp", json={"request_key": res["request_key"], "otp": pyotp.TOTP(totp_key).now()}).json()
        
        # 3. Verify PIN
        res = req.post(f"{BASE_2}/verify_pin", json={"request_key": res["request_key"], "identity_type": "pin", "identifier": pin}).json()
        temp_token = res["data"]["access_token"]
        
        # 4. Get Auth Code
        payload = {"fyers_id": fy_id, "app_id": app_id, "redirect_uri": redirect_uri, "appType": app_type, "code_challenge": "", "state": "sample_state", "scope": "", "nonce": "", "response_type": "code", "create_cookie": True}
        res = req.post(f"{BASE_3}/token", json=payload, headers={'Authorization': f'Bearer {temp_token}'})
        auth_code = parse_qs(urlparse(res.json()["Url"]).query)['auth_code'][0]
        
        # 5. Get Access Token
        session = fyersModel.SessionModel(client_id=client_id, secret_key=secret_key, redirect_uri=redirect_uri, response_type='code', grant_type='authorization_code')
        session.set_token(auth_code)
        access_token = session.generate_token()["access_token"]
        
        # 6. Save to .simple.env
        set_key(env_path, "access_token", access_token)
        print("Access token successfully generated and saved to .simple.env")
        return access_token

    except Exception as e:
        print(f"Error generating token: {e}")
        return None

if __name__ == "__main__":
    access_token_generator()