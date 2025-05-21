from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import  FlightData
from notification_manager import NotificationManager
dm = DataManager()
fs = FlightSearch()
fd = FlightData()
nm = NotificationManager()
sheet_data = dm.get_sheet_data()

def main():
    for row in sheet_data["prices"]:
        if row["iataCode"] == "" or row["iataCode"] == "TESTING":
            city = row["city"]
            iata_code = fs.get_city_info(city)
            dm.update_iata_code(row["id"], iata_code)
        iata_code = row["iataCode"]
        lowest_price = int(row["lowestPrice"])
        flights = fs.search_flights(iata_code, lowest_price)
        if flights["data"]:
            sorted_flights = sorted(flights["data"], key=lambda f: float(f["price"]["grandTotal"]))
            first_flight = sorted_flights[0]
            itineraries = first_flight["itineraries"]
            price = first_flight["price"]
            flight_infos =fd.structured_data(itineraries, price)
            notification = nm.send_message(flight_infos)



if __name__ == "__main__":
    main()



















