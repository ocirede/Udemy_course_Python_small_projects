import requests
import time
import os
from dotenv import load_dotenv


load_dotenv()
class AmadeusToken:
    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.token = None
        self.token_expiry = 0

    def get_access_token(self):
        if self.token and time.time() < self.token_expiry:
            return self.token

        response = requests.post(
            "https://test.api.amadeus.com/v1/security/oauth2/token",

        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id ,
            "client_secret": self.client_secret
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
        )
        response.raise_for_status()
        data = response.json()
        self.token = data["access_token"]
        self.token_expiry = time.time() + data["expires_in"] - 60
        return self.token
