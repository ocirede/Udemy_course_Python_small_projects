class FlightData:
    def structured_data(self, itineraries, price):
        segments_info = []
        for itinerary in itineraries:
            for segment in itinerary["segments"]:
                dep = segment['departure']['iataCode']
                dep_time = segment['departure']['at'][11:16]
                arr = segment['arrival']['iataCode']
                arr_time = segment['arrival']['at'][11:16]
                carrier = segment['carrierCode']
                flight_no = segment['number']

                seg_text = f"{dep}({dep_time})→{arr}({arr_time}) {carrier}{flight_no}"
                segments_info.append(seg_text)

        segments_str = "; ".join(segments_info)
        price_str = f"Total: {price['grandTotal']}€"

        message = f"{segments_str}\n{price_str}"
        return message
