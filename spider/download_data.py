import json
import os
import requests

'''Script for downloading data from API links'''


jl_path = "file.jl"
downloads_dir = "downloads/full"

os.makedirs(downloads_dir, exist_ok=True)

def download_csv(url, path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            print(f"Downloaded: {path}")
        else:
            print(f"Failed to download {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while downloading {url}. Error: {e}")

with open(jl_path, 'r') as file:
    for line in file:
        data = json.loads(line)
        for title, url in data.items():
            safe_title = "".join([c if c.isalnum() else "_" for c in title])
            
            csv_path = os.path.join(downloads_dir, f"{safe_title}.csv")

            download_csv(url, csv_path)
