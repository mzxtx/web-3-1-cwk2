# login interface
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from exts import db
from model import UserModel, ServeModel
from .form import Sign_up_Form, Sign_in_Form, Serve_Form

bp = Blueprint("user", __name__, url_prefix="/user")


# sign in
@bp.route("/sign_in", methods=['GET', 'POST'])
def sign_in():
    if request.method == 'GET':
        return render_template("sign_in.html")
    else:
        form = Sign_in_Form(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            adm = UserModel.query.filter_by(email="Charlie@adm.com")[0]
            if adm and adm.password == password:
                session['user_id'] = adm.id
                return redirect(url_for("user.adm_user"))
            elif user and user.password == password:
                session['user_id'] = user.id
                return redirect(url_for("user.index_user"))
            else:
                flash("The email address and password do not match.")
                return redirect(url_for("user.sign_in"))
        else:
            flash("The email or password format is incorrect.")
            return redirect(url_for("user.sign_in"))


# sign up
@bp.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template("sign_up.html")
    else:
        form = Sign_up_Form(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data

            user = UserModel(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.sign_in"))
        else:
            email = form.email.data
            user_model = UserModel.query.filter_by(email=email).first()
            if user_model:
                flash("The email address has been registered.")
            else:
                flash("The message format is incorrect.")
            return redirect(url_for("user.sign_up"))


# sign out
@bp.route("/sign_out")
def sign_out():
    # Clear all data in the session
    session.clear()
    return redirect(url_for('user.sign_in'))


# user interface
@bp.route("/index")
def index_user():
    return render_template("index-user.html")


# Administrator Interface
@bp.route("/adm/user")
def adm_user():
    return render_template("adm-user.html")


# Administrator Interface - Serve
@bp.route("/adm/serve")
def adm_serve():
    serves = ServeModel.query.all()
    return render_template("adm-serve.html",serves=serves)


# add serve
@bp.route("/adm/serve/add", methods=['GET', 'POST'])
def serve_add():
    if request.method == 'GET':
        return render_template("add_serve.html")
    else:
        form = Serve_Form(request.form)
        if form.validate():
            servename = form.servename.data
            classification = form.classification.data
            obj = form.obj.data
            price = form.price.data
            introduction = form.introduction.data

            serve = ServeModel(servename=servename, classification=classification, obj=obj, price=price,
                               introduction=introduction)
            db.session.add(serve)
            db.session.commit()
            return redirect(url_for("user.adm_serve"))
        else:
            flash("The message format is incorrect.")
            return redirect(url_for("user.serve_add"))
