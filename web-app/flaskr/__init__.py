from flask import Flask, render_template, jsonify
from flaskr.db import get_translations_collection
from pymongo import MongoClient
import os

def create_app(test_config=None):
    app = Flask(__name__)
    
    if (test_config == None):
        conn_str = os.getenv('DB_URL', 'mongodb://localhost:27017')
        app.config.from_mapping(
            MONGO_CLIENT=MongoClient(conn_str)
        )
    else:
        app.config.from_mapping(test_config)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/history")
    def history():
        cursor = get_translations_collection(app.config['MONGO_CLIENT']).find()
        history_data = list(cursor)
        cursor.close()
        return render_template("history.html", history=history_data)

    @app.route("/translation")
    def translation():
        translation = get_translations_collection(app.config['MONGO_CLIENT']).find_one(sort=[('_id', -1)])
        if (translation == None):
            return jsonify({})
        translation.pop("_id") # Pop _id field because jsonify has no clue what to do with it.
        return jsonify(translation)

    return app
