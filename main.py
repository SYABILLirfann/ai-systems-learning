import requests


def search_city(city):

    search_parameters = {
    "name": city
     }


    try:
    
         response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
         params=search_parameters
         )

         if response.status_code == 200:
    
            whole_data = response.json()

            if"results" in whole_data:


             print (f"City:{whole_data['results'][0]['name']}")
             print (f"Country:{whole_data['results'][0]['country']}")
             print (f"Latitude:{whole_data['results'][0]['latitude']}")
             print (f"Longitude:{whole_data['results'][0]['longitude']}")


            else:
             print ("Location not found.")
 


         else:
            print(f"API error:{response.status_code}")


    except requests.RequestException:
          print("Could not connect to the API.")

city = input("Enter a city: ")

search_city(city)