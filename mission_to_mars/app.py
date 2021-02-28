from flask import Flask, render_template, redirect
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

    mars_data = client.db.collection.find_one()
    return render_template("index.html", mars=mars_data)


# Route for scrape function
@app.route("/scrape")
def scrape():

    
    mars_data = mission_to_mars.scrape_mars()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)