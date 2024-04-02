import argparse
import pandas as pd
import pickle
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Parse arguments for MongoDB connection
parser = argparse.ArgumentParser(description='Model Water Consumption per Inhabitant based on Population Size Class')
parser.add_argument('-u', '--uri', required=True, help="mongodb uri with username/password")
args = parser.parse_args()

# Connect to MongoDB
client = MongoClient(args.uri)
db = client['bfs']
collection = db['bfs_data']

# Fetch and process data from MongoDB
documents = collection.find({
    'VALUE_PERIOD': {'$in': ['2020']},
    'GEO_NR': {'$ne': 'CH'}
})

# Convert documents to DataFrame
df = pd.DataFrame(list(documents))

print(df)

# Replace empty strings with NaN in 'VALUE' and convert to numeric
df['VALUE'] = pd.to_numeric(df['VALUE'], errors='coerce').fillna(0)

df_pivoted = df.pivot_table(index=['GEO_NR', 'CLASS_HAB'], columns='VARIABLE', values='VALUE', aggfunc='first').reset_index().fillna(0)
print(df_pivoted)

df_pivoted[df_pivoted.select_dtypes(include=['object']).columns] = df_pivoted.select_dtypes(include=['object']).apply(pd.to_numeric, errors='coerce')

# Prepare data for model
X = df_pivoted.drop(columns=['CLASS_HAB', 'GEO_NR', 'wlivr_max', 'deb_hj_max', 'wcapt_sout'])  # Removed redundant columns listed
y = df_pivoted['CLASS_HAB'].astype(int)  # Convert target column to integer for classification
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training and predictions
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save the model
model_filename = 'random_forest_model.pkl'
with open(model_filename, 'wb') as model_file:
    pickle.dump(clf, model_file)


def predict_population_class(input_features):
    with open(model_filename, 'rb') as model_file:
        loaded_model = pickle.load(model_file)
    input_df = pd.DataFrame([input_features], columns=X.columns)
    return loaded_model.predict(input_df)[0]