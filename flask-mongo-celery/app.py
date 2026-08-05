import os

from celery import Celery
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_pymongo import PyMongo

MONGODB_DATABASE_URL = os.environ.get(
    "MONGODB_URI", "mongodb://localhost:27017/mars_app"
)

# Initialize the flask app
app = Flask(__name__)

app.config["MONGO_URI"] = MONGODB_DATABASE_URL

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app)

celery = Celery(app.name)
celery.conf.update(
    broker_url=os.environ.get("CELERY_BROKER_URL", MONGODB_DATABASE_URL),
    result_backend=os.environ.get("CELERY_RESULT_BACKEND", MONGODB_DATABASE_URL),
)


import scraping


@app.route("/", methods=["GET", "POST"])
def index():
    mars = mongo.db.mars_app.find_one()
    if request.method == "GET":
        return render_template("index.html", mars=mars)
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
