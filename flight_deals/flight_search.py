import requests
from token_update import AmadeusToken
from datetime import datetime, timedelta


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

    def search_flights(self, iata_code, lowest_price, days_back=3):
        base_departure_date = datetime.strptime("2026-01-31", "%Y-%m-%d")
        base_return_date = datetime.strptime("2026-02-21", "%Y-%m-%d")
        trip_length = (base_return_date - base_departure_date).days

        for i in range(days_back + 1):
            departure_date = base_departure_date - timedelta(days=i)
            return_date = departure_date + timedelta(days=trip_length)

            params = {
                "originLocationCode": "BER",
                "destinationLocationCode": iata_code,
                "departureDate": departure_date.strftime("%Y-%m-%d"),
                "returnDate": return_date.strftime("%Y-%m-%d"),
                "adults": 1,
                "maxPrice": lowest_price,
                "currencyCode": "EUR"
            }

            print(f"Trying: {params['departureDate']} -> {params['returnDate']}")
            response = requests.get(url=self.flight_search, params=params, headers=self.headers)
            data = response.json()

            if data.get("data"):
                return data

        return {"data": [], "message": "No results found in the given range."}





