from flask import Flask, render_template, jsonify
from db import translations

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
