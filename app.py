#%%
# Mongo works well with python and Flask
# Flask is framework for developers that helps inbuildiing web apps
# import dependencies/libraries
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
# %%
# let us set up flask
app = Flask(__name__)

# %%
# lets tell python how to connect to mongo using PyMongo
# use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
# %%
# next we set up Flask route
# 1. for everyone to view when visiting the page--ourpage.com/
# 2. one for scraping---ourpage.com/scrape
# the routes will be embended in the webpage and accessed via links and buttons
@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)
# %%
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)
# %%
mars.update({}, mars_data, upsert=True)
# %%
if __name__ == "__main__":
   app.run()
# %%
