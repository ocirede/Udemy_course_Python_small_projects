import requests
from token_update import AmadeusToken


class FlightSearch:
    def __init__(self):
        at = AmadeusToken()
        self.flight_search_token = at.get_access_token()
        self.flight_endpoint = "https://test.api.amadeus.com/v1/reference-data/locations/cities?"
        self.flight_search = "https://test.api.amadeus.com/v2/shopping/flight-offers?"
        self.headers = {
            "Authorization": f"Bearer {self.flight_search_token}"
        }
    def get_city_info(self, city_name):
            params = {"keyword": city_name}
            response = requests.get(url=self.flight_endpoint, params=params, headers=self.headers)
            data = response.json()
            print(f"API response for {city_name}: {data}")
            try:
                for location in data["data"]:
                    iata_code = location["iataCode"]
                    if iata_code:
                        return iata_code
            except Exception as e:
                    print(f"Error fetching IATA code for {city_name}: {e}")
            return "TESTING"

    def search_flights(self, iata_code, lowest_price):
        params = {
            "originLocationCode": "BER",
            "destinationLocationCode": iata_code,
            "departureDate": "2026-02-01",
            "adults": 1,
            "maxPrice": lowest_price,
            "currencyCode": "EUR"
        }
        response = requests.get(url=self.flight_search, params=params, headers=self.headers)
        print(response.status_code)
        data = response.json()
        return data





