import requests
import os
import json
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def get_coordinates(address, api_key):
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
        return latitude, longitude
    else:
        return None, None

def process_data(api_key):
    with open("data.json") as file:
        data = json.load(file)
    
    addresses = [item["address"] for item in data]

    coords = []
    
    for addr in addresses:
        coords.append(get_coordinates(addr, api_key))
    
    X = [[lon, lat] for lon, lat in coords]

    min_clusters = 2 
    max_clusters = len(X) -1

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

    print(dyct)

def main():
    api_key = os.environ['google_map_api_key']
    
    process_data(api_key)

if __name__ == "__main__":
    main()