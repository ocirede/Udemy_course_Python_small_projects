import requests
import os
from dotenv import load_dotenv

load_dotenv()
class DataManager:
    def __init__(self):
        self.sheety_token = os.getenv("SHEETY_TOKEN")
        self.endpoint = "https://api.sheety.co"
        self.prices = "f489ed90d1332f35a23104bb935a9b5e/flightDeals/prices"
        self.headers = {
            "Authorization": f"Basic {self.sheety_token}"
        }


    def get_sheet_data(self):
        try:
            response = requests.get(url=f"{self.endpoint}/{self.prices}", headers=self.headers)
            print(response.status_code)
            data = response.json()
            return data
        except Exception as e:
            print(e)

    def update_iata_code(self, row_id, iata_code):
        body = {
            "price": {
                "iataCode": iata_code
            }
        }
        response = requests.put(url=f"{self.endpoint}/{self.prices}/{row_id}", json=body, headers=self.headers)
        response.raise_for_status()




