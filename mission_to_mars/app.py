
from flask import Flask, jsonify, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    mars_info = client.db.scraped_mars.find_one()
    return render_template("index.html", mars_info=mars_info)


# Route for scrape function
@app.route("/scrape")
def scrape():

    
    db = client.db.scrape_mars
    mars_data = scrape_mars.scrape()
    db.update({}, mars_data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)