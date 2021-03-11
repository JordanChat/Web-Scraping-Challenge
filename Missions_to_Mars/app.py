from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri = "mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars_things = mongo.db.collection.find_one()

    return render_template("index.html", mars_things = mars_things)

@app.route("/scrape")
def scrape():
    mars_things = scrape_mars.scrape()

    mongo.db.collection.update({}, mars_things, upsert = True)

    return redirect("/")

    


if __name__ == "__main__":
    app.run(debug=True)