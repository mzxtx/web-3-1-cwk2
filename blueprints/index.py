# pet page
from flask import Blueprint,render_template,g,request
from model import ServeModel
from sqlalchemy import or_

bp = Blueprint("index",__name__,url_prefix="/")

# index
@bp.route("/")
def index():
    return render_template("index/index.html")

# serve
@bp.route("/serve")
def serve():
    serves = ServeModel.query.all()
    return render_template("index/serve.html",serves=serves)

# serve detail
@bp.route("/serve/detail/<int:serve_id>")
def serve_detail(serve_id):
    serve = ServeModel.query.get(serve_id)
    return render_template("index/serve_detail.html", serve=serve)

# search serve
@bp.route("/search_serve")
def search_serve():
    query = request.args.get("query")
    serves = ServeModel.query.filter(or_(ServeModel.servename.contains(query),
                                              ServeModel.classification.contains(query),
                                              ServeModel.obj.contains(query),
                                              ServeModel.price.contains(query),))

    return render_template("index/serve.html", serves=serves)