from pymongo import MongoClient
import json
client = MongoClient('mongodb://localhost:27017')

db = client.translator
translations = db.translations

if __name__ == "__main__":
    # import sample data into the database
    with open('sample_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        translations.insert_many(data)
