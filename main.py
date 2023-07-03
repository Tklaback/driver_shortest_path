import requests
import os
import json
import re
from graph import Graph, Vertex

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
    if data["status"] == "OK":
        route = data["routes"][0]
        duration = route["legs"][0]["duration"]["text"]
        distance = route["legs"][0]["distance"]["text"]
        # steps = route["legs"][0]["steps"]
        # print(f"Total Distance: {distance}")
        # print(f"Total Duration: {duration}")
        # print("Steps:")
        # for i, step in enumerate(steps, 1):
        #     print(f"Step {i}: {step['html_instructions']}")
    return duration, distance
    



def build_graph(api_key) -> Graph:
    graph = Graph()

    # Open the JSON file
    with open("data.json") as file:
        data = json.load(file)

    # Iterate over the list of objects and access the addresses

    addresses = [item["address"] for item in data]

    with open("home_address.txt") as f:
        addresses.append(f.readline())

    for address in addresses:
        for other_address in addresses:
            if other_address != address:
                data = get_directions(address, other_address, api_key)

                duration_regex = r'(\d+)\s*(hour|min|second)s?'
                matches = re.findall(duration_regex, data[0])
                duration = 0
                for match in matches:
                    value, unit = match
                    value = int(value)
                    if unit == "hour":
                        duration += value * 3600
                    elif unit == "min":
                        duration += value * 60
                # print(data[0], duration)
                graph.add_edge(address, other_address, duration)
    return graph

    

def main():

    api_key = os.environ["google_maps_api_key"]

    g = build_graph(api_key)

    home_vertex = g.get_vertex("360 Wymount Terrace, Provo, UT")

    g.shortest_travel_path(home_vertex, 0, [], [], home_vertex)


if __name__ == "__main__":
    main()






