import requests

def search_location(location):
    search_parameters ={
        "name": location
    }
    try:
       response = requests.get(
       "https://geocoding-api.open-meteo.com/v1/search",
       params=search_parameters
       )
       if response.status_code == 200:
           whole_data = response.json()

           if "results" in whole_data:

               location_data = {
                   "name": whole_data["results"][0]["name"],
                   "country": whole_data["results"][0]["country"],
                   "latitude": whole_data["results"][0]["latitude"],
                   "longitude": whole_data["results"][0]["longitude"]
                    }


               return location_data
           else:
               return None

       else:

        return None

    except requests.RequestException:
        return None

def build_travel_report(location_data):
    travel_report = {
        "destination": location_data["name"],
        "country": location_data["country"],
        "latitude": location_data["latitude"],
        "longitude": location_data["longitude"]
    }

    return travel_report

def send_report(travel_report):

    try:

        response = requests.post(
            "https://jsonplaceholder.typicode.com/posts",
            json = travel_report
        )

        if response.status_code == 201:

            returned_data = response.json()
            return returned_data

        else:
            return None

    except requests.RequestException:
        return None

location = input("Enter a destination: ")

location_data = search_location(location)

if location_data:
    travel_report = build_travel_report(location_data)
    report_result = send_report(travel_report)

    if report_result:
        print("Travel report sent successfully!")
    else:
        print("Travel report failed.")

else:
    print("Location not found")