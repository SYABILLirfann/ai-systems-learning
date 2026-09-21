import requests

city = input("Enter a city:")


search_parameters = {
    "name": city
}
try:

    response = requests.get ("https://geocoding-api.open-meteo.com/v1/search",
                         params = search_parameters)


    if response.status_code == 200:
       print("API connected!")

       whole_data = response.json()

       if "results" in whole_data:

          print(f"city: {whole_data["results"][0]["name"]}")
          print(f"Country: {whole_data["results"][0]["country"]}")
          print(f"Latitude: {whole_data["results"][0]["latitude"]}")
          print(f"Longitude: {whole_data["results"][0]["longitude"]}")

          city_report = {
          "city": whole_data["results"][0]["name"],
          "country": whole_data["results"][0]["country"],
          "latitude": whole_data["results"][0]["latitude"],
          "longitude": whole_data["results"][0]["longitude"]
           }    


          try:
                send_response = requests.post(
                   "https://jsonplaceholder.typicode.com/posts",
                    json=city_report
                ) 

                if send_response.status_code == 201:
                  returned_data = send_response.json()
                  print(f"Report ID: {returned_data['id']}")

                else:
                  print(f"POST API error: {send_response.status_code}")

          except requests.RequestsException:
                print("Could not connect to the POST API.")
          
       else:
           print("Location not found")

    else:
      print(f"API error: {response.status_code}")


except requests.RequestException:
    print("Could not connect to the API.")

