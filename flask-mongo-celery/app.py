# Import Dependencies
from celery import Celery
from flask import Flask, render_template, redirect
from flask.globals import request
from flask.helpers import url_for
from flask.json import jsonify
from flask_pymongo import PyMongo

# update with every project
DB_NAME = "mars_app"
MONGODB_URL = "mongodb://localhost:27017/"

# mongodb connection string
MONGODB_DATABASE_URL = f"{MONGODB_URL}{DB_NAME}"

# Initialize the flask app
app = Flask(__name__)

app.config["broker_url"] = MONGODB_DATABASE_URL
app.config["result_backend"] = MONGODB_DATABASE_URL

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

celery = Celery(
    app.name, backend=app.config["result_backend"], broker=app.config["broker_url"]
)
celery.conf.update(app.config)


import scraping


@app.route("/", methods=["GET", "POST"])
def index():
    mars = mongo.db.mars_app.find_one()
    if request.method == "GET":
        return render_template("index.html", mars=mars)
    elif request.method == "POST":
        return redirect(url_for("index"))


# # Originally we have a route that runs the web harvesting function
# # but I converted it to a status check route below.
# @app.route("/scrape")
# def scrape():
#     # Fix this variable and process
#     success = scraping.scrape_all()
#     return jsonify(success)


@app.route("/longtask", methods=["POST"])
def longtask():
    task = scraping.scrape_all.apply_async()
    return jsonify({}), 202, {"Location": url_for("taskstatus", task_id=task.id)}


@app.route("/status/<task_id>", methods=["GET"])
def taskstatus(task_id=None):
    task = scraping.scrape_all.AsyncResult(task_id)
    response = {
        "state": task.state,
    }
    return jsonify(response)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
