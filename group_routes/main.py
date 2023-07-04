import requests
import os
import json
from sklearn.cluster import KMeans
from datetime import datetime
from sklearn.metrics import silhouette_score
import numpy as np
from st_dbscan import ST_DBSCAN

time_format = "%Y-%m-%dT%H:%M:%S%z"

def get_coordinates(address, api_key, time):
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
        time = datetime.strptime(time, time_format)
        time_int = int(time.timestamp())
        return latitude, longitude, time_int
    else:
        return None, None

def process_data(api_key):
    with open("data.json") as file:
        data = json.load(file)
    
    addresses = [(item["address"], item['time']) for item in data]

    coords = []
    
    for addr in addresses:
        coords.append(get_coordinates(addr[0], api_key, addr[1]))
    
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
        if labels[idx] in dyct:
            dyct[labels[idx]].append(addresses[idx])
        else:
            dyct[labels[idx]] = [addresses[idx]]

    return dyct

def main():
    api_key = os.environ['google_map_api_key']
    
    processed_dyct = process_data(api_key)

    print(processed_dyct)

    averages = {}
    for key, values in processed_dyct.items():
        total_seconds = sum([datetime.fromisoformat(time).timestamp() for _, time in values])
        average_seconds = total_seconds / len(values)
        averages[key] = average_seconds
    
    print(averages)
    
    key_with_smallest_value = min(averages, key=averages.get)


    print(key_with_smallest_value)

if __name__ == "__main__":
    main()