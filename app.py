from flask import Flask
app = Flask(__name__)

@app.route("/")
def welcome():
    return"Welcome to this Site"

@app.route("/home")
def home():
    return"This is Home Page"

# import controller.user_controller as user_controller
# import controller.user_product as user_product
from controller import *