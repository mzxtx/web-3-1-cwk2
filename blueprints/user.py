# login interface
from flask import Blueprint

bp = Blueprint("user",__name__,url_prefix="/user")

@bp.route("/login")
def login():
    return "login"