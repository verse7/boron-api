from flask import Blueprint
from application import db
from application.services.menuService import MenuService

api_bp = Blueprint('api_bp', __name__, url_prefix="/api")  

@api_bp.route("/menu/<vendor>", methods=['GET'])
@api_bp.route("/menu/<vendor>&<mode>", methods=['GET'])
def menu(vendor, mode="simple"):
    domain = "@gmail.com"
    menu = MenuService(vendor + domain)
    return menu.toJSON(mode)
    