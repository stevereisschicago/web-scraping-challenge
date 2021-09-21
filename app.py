from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create Flask
app = Flask(__name__)

# :  Using info from 12.3.10
# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_info = mongo.db.collection.find_one()
    # mars_info = list(mongo.db.collection.find())
    print(mars_info)

    # Return template and data
    return render_template("index.html", mars=mars_info)
  

# Route that will trigger the scrape function
@app.route("/scrape")
def scraper():
    # mars_info = mongo.db.collection
    # Run the scrape function
    mars_data = scrape_mars.scrape_info()
    
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

   # Test and print
   # print(mars_info, flush=True)

if __name__ == "__main__":
    app.run(debug=True)

