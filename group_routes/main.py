import requests
import os
import json
from sklearn.cluster import KMeans
from datetime import datetime
from sklearn.metrics import silhouette_score
import numpy as np
from st_dbscan import ST_DBSCAN
from math import sqrt

time_format = "%Y-%m-%dT%H:%M:%S%z"

def get_coordinates(address, api_key, time=None):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        latitude = location["lat"]
        longitude = location["lng"]
        if time:
            time = datetime.strptime(time, time_format)
            time_int = int(time.timestamp())
            return latitude, longitude, time_int
        else:
            return latitude, longitude
    else:
        return None, None

def process_data(api_key):
    with open("data.json") as file:
        data = json.load(file)
    
    addresses = [(item["address"], item['time']) for item in data]

    coords = []
    
    for addr in addresses:
        address_coords = get_coordinates(addr[0], api_key, addr[1])
        coords.append(address_coords)
    
    X = [[lon, lat, time] for lon, lat, time in coords]

    min_clusters = 2 
    max_clusters = len(X) - 1

    best_num_clusters = None
    best_silhouette_score = -1

    # Iterate over different values of num_clusters
    for num_clusters in range(min_clusters, max_clusters+1):
        # Create a K-means clustering model
        kmeans = KMeans(n_clusters=num_clusters, n_init=10)

        # Fit the model to the data
        kmeans.fit(X)

        # Get the cluster labels for each coordinate
        labels = kmeans.labels_

        # Calculate the silhouette score
        silhouette_avg = silhouette_score(X, labels)

        # Update the best_num_clusters and best_silhouette_score if applicable
        if silhouette_avg > best_silhouette_score:
            best_num_clusters = num_clusters
            best_silhouette_score = silhouette_avg

    kmeans = KMeans(n_clusters=best_num_clusters, n_init=10)

    kmeans.fit(X)

    labels = kmeans.labels_

    dyct = {}

    for idx in range(len(addresses)):
        final_tupl = [item for item in addresses[idx]]
        final_tupl.append(coords[idx][:-1])
        if labels[idx] in dyct:
            dyct[labels[idx]].append(tuple(final_tupl))
        else:
            dyct[labels[idx]] = [tuple(final_tupl)]

    return dyct

def calculate_average_time(items):
    total_seconds = sum([datetime.fromisoformat(item[1]).timestamp() for item in items])
    average_seconds = total_seconds / len(items)
    return average_seconds

# Define a function to calculate the centroid distance
def calculate_centroid_distance(items):
    latitudes = [item[2][0] for item in items]
    longitudes = [item[2][1] for item in items]
    centroid_latitude = sum(latitudes) / len(latitudes)
    centroid_longitude = sum(longitudes) / len(longitudes)
    return (centroid_latitude, centroid_longitude)


def main():
    api_key = os.environ['google_map_api_key']
    home_address = os.environ['home_address']
    
    processed_dyct = process_data(api_key)

    home_coordinates = get_coordinates(home_address, api_key)

    # Sort dictionary first by the average time and then by dist from 
    # current location in value of each key, value pair.
    sorted_data = {k: v for k, v in sorted(processed_dyct.items(), key=lambda item: (calculate_average_time(item[1]), sqrt((calculate_centroid_distance(item[1])[0] - home_coordinates[0]) ** 2 + (calculate_centroid_distance(item[1])[1] - home_coordinates[1]) ** 2)))}

    for lst in sorted_data:
        print(sorted_data[lst], "\n")

if __name__ == "__main__":
    main()