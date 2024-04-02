import csv
from pymongo import MongoClient
import os
from pathlib import Path

def detect_delimiter(csv_file):
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        sample = file.read(1024)
        sniffer = csv.Sniffer()
        return sniffer.sniff(sample).delimiter

def csv_to_documents(file_path):
    documents = []
    delimiter = detect_delimiter(file_path)
    with open(file_path, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            documents.append(row)
    return documents

def import_csv_to_mongodb(directory, mongo_uri, db_name, collection_name):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    for csv_file in os.listdir(directory):
        if csv_file.endswith('.csv'):
            file_path = Path(directory, csv_file)
            documents = csv_to_documents(file_path)
            if documents:
                collection.insert_many(documents)
                print(f"Inserted documents from {csv_file}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--uri', required=True, help="MongoDB URI with username/password")
    parser.add_argument('-d', '--directory', required=True, help="Directory containing CSV files")
    parser.add_argument('-db', '--database', required=True, help="Name of the MongoDB database")
    parser.add_argument('-c', '--collection', required=True, help="Name of the MongoDB collection")
    
    args = parser.parse_args()
    import_csv_to_mongodb(args.directory, args.uri, args.database, args.collection)
