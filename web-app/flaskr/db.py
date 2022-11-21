import pymongo
import json

def get_translations_collection(client):
    db = client.translator
    return db.translations

def insert_sample_data(client, fn='sample_data.json'):
    with open(fn, 'r', encoding='utf-8') as f:
        data = json.load(f)
        get_translations_collection(client).insert_many(data)

if __name__ == "__main__":
    # import sample data into the database
    insert_sample_data(pymongo.MongoClient('mongodb://localhost:27017'))
    
