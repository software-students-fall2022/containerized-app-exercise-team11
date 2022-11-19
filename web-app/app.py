from flask import Flask, render_template
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
