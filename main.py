import requests
import os

def get_directions(origin, destination, api_key):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": "driving",
        "key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    print(data)
    if data["status"] == "OK":
        route = data["routes"][0]
        duration = route["legs"][0]["duration"]["text"]
        distance = route["legs"][0]["distance"]["text"]
        steps = route["legs"][0]["steps"]
        print(f"Total Distance: {distance}")
        print(f"Total Duration: {duration}")
        print("Steps:")
        for i, step in enumerate(steps, 1):
            print(f"Step {i}: {step['html_instructions']}")
    

api_key = os.environ["google_maps_api_key"]






