from api import app, db
from api import Menu

@app.route("/")
@app.route("/home")
def home():
    return {"msg": "hello"}


@app.route("/menu/<vendor>", methods=['GET'])
@app.route("/menu/<vendor>&<mode>", methods=['GET'])
def menu(vendor, mode="simple"):
    domain = "@gmail.com"
    menu = Menu(vendor + domain)
    return menu.toJSON(mode)