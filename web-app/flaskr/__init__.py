from flask import Flask, render_template, jsonify
from flaskr.db import translations

def create_app(test_config=None):

    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/history")
    def history():
        cursor = translations.find()
        history_data = list(cursor)
        cursor.close()
        return render_template("history.html", history=history_data)

    @app.route("/translation")
    def translation():
        translation = translations.find_one(sort=[('_id', -1)])
        translation.pop("_id") # Pop _id field because jsonify has no clue what to do with it.
        return jsonify(translation)

    return app
