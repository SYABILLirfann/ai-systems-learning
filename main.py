import requests


try:

    response = requests.get("https://api.github.com")


    print(response.status_code)

    if response.status_code == 200:
       print("API connected!")    
    
       data = response.json()
       print(f"Repository API : {data['repository_url']}")

    else:
        print("API error!")

    
except requests.RequestException:

    print("An error occurred:")



