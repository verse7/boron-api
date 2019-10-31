from api import app, db
from api import Menu

@app.route("/")
@app.route("/home")
def home():
    return {"msg": "hello"}

@app.route("/menu/<vendor>", methods=['GET'])
def menu(vendor):
    domain = "@gmail.com"
    menu = Menu(vendor + domain)
    return menu.toJSON()