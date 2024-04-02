# python -m flask --debug --app service run (works also in PowerShell)

import datetime
import os
import pickle
from pathlib import Path

import pandas as pd
from azure.storage.blob import BlobServiceClient
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

# init app, load model from storage
print("*** Init and load model ***")
if 'AZURE_STORAGE_CONNECTION_STRING' in os.environ:
    azureStorageConnectionString = os.environ['AZURE_STORAGE_CONNECTION_STRING']
    blob_service_client = BlobServiceClient.from_connection_string(azureStorageConnectionString)

    print("fetching blob containers...")
    containers = blob_service_client.list_containers(include_metadata=True)
    for container in containers:
        existingContainerName = container['name']
        print("checking container " + existingContainerName)
        if existingContainerName.startswith("bfs-model"):
            parts = existingContainerName.split("-")
            print(parts)
            suffix = 1
            if (len(parts) == 3):
                newSuffix = int(parts[-1])
                if (newSuffix > suffix):
                    suffix = newSuffix

    container_client = blob_service_client.get_container_client("bfs-model-" + str(suffix))
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)

    # Download the blob to a local file
    Path("../model").mkdir(parents=True, exist_ok=True)
    download_file_path = os.path.join("../model", "random_forest_model.pkl")
    print("\nDownloading blob to \n\t" + download_file_path)

    with open(file=download_file_path, mode="wb") as download_file:
         download_file.write(container_client.download_blob(blob.name).readall())

else:
    print("CANNOT ACCESS AZURE BLOB STORAGE - Please set connection string as env variable")
    print(os.environ)
    print("AZURE_STORAGE_CONNECTION_STRING not set")    

file_path = Path(".", "../model/", "random_forest_model.pkl")
with open(file_path, 'rb') as fid:
    model = pickle.load(fid)
    
print("*** Init Flask App ***")
app = Flask(__name__)
cors = CORS(app)
app = Flask(__name__, static_url_path='/', static_folder='../frontend/build')

@app.route("/")
def indexPage():
    return send_file("../frontend/build/index.html")  

@app.route("/api/predict_population_class", methods=['POST'])
def predict_population_class():
    # Retrieve feature values from the request's form or JSON
    feature_values = request.json or request.form
    required_features = ['deb_hj_moy', 'gaz_t', 'wcapt_lac_riv', 'wcapt_sour', 'wcapt_t', 'wlivr_moy']
    
    # Extract the features from the request
    input_features = [float(feature_values.get(feature, 0)) for feature in required_features]
    
    # Create DataFrame from input features
    input_df = pd.DataFrame([input_features], columns=required_features)
    
    # Predict the population class
    prediction = model.predict(input_df)[0]
    
    # Respond with the predicted class
    return jsonify({
        'predicted_class': int(prediction)  # Convert to int for JSON serialization
    })

if __name__ == "__main__":
    app.run(debug=True)