from flask import Blueprint, current_app as app

main_bp = Blueprint('main_bp', __name__)

@app.route("/")
@app.route("/home")
def home():
    return {"msg": "hello"}