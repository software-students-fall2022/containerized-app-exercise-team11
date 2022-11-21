import pymongo
import json

def get_translations_collection(client):
    db = client.translator
    return db.translations

if __name__ == "__main__":
    # import sample data into the database
    client = pymongo.MongoClient('mongodb://localhost:27017')
    with open('sample_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        get_translations_collection(client).insert_many(data)
