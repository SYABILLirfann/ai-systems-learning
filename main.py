import requests

def search_location(location):
    search_parameters = {"name": location}

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
                                 "longitude": whole_data["results"][0]["longitude"],
                                }
                return location_data
            
            else:
                return None
        else:
            return None
    except requests.RequestException:
        return None



def get_weather(location_data):
    latitude = location_data["latitude"]
    longitude = location_data["longitude"]

    weather_parameters = {
    "latitude": latitude,
    "longitude": longitude,
    "current": "temperature_2m,wind_speed_10m,weather_code"
     } 


    try:
        weather_response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params=weather_parameters
    )
        if weather_response.status_code == 200:
            weather_data = weather_response.json()

            temperature = weather_data["current"]["temperature_2m"]
            wind_speed = weather_data["current"]["wind_speed_10m"]
            weather_code = weather_data["current"]["weather_code"]


            weather_info = {
                            "temperature": temperature,
                            "wind_speed": wind_speed,
                            "weather_code": weather_code
                            }

            return weather_info

        else:
            return None

    except requests.RequestException:
        return None


def build_weather_report(location_data, weather_info):
    report = {
    "destination": location_data["name"],
    "country": location_data["country"],
    "temperature": weather_info["temperature"],
    "wind_speed": weather_info["wind_speed"],
    "weather_code": weather_info["weather_code"],
}

    return report



location = input("Enter a destination: ")

location_data = search_location(location)

if location_data:
    weather_info = get_weather(location_data)

    if weather_info:
        report = build_weather_report(location_data, weather_info)

        print(f"Destination: {report['destination']}")
        print(f"Country: {report['country']}")
        print(f"Temperature: {report['temperature']}")
        print(f"Wind Speed: {report['wind_speed']}")
        print(f"Weather Code: {report['weather_code']}")

    else:
        print("Weather could not be found")

else:
    print("Location could not be found")