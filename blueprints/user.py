# login interface
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from exts import db
from model import UserModel, ServeModel, PetModel
from .form import Sign_up_Form, Sign_in_Form, Serve_Form, Add_User_Form, Edit_User_Form
from sqlalchemy import or_

bp = Blueprint("user", __name__, url_prefix="/user")


# sign in
@bp.route("/sign_in", methods=['GET', 'POST'])
def sign_in():
    if request.method == 'GET':
        return render_template("index/sign_in.html")
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
        return render_template("index/sign_up.html")
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
    return render_template("user/index-user.html")


# user serve
@bp.route("/serve")
def serve():
    serves = ServeModel.query.all()
    return render_template("user/serve.html", serves=serves)


# serve detail
@bp.route("/serve/detail/<int:serve_id>")
def serve_detail(serve_id):
    serve = ServeModel.query.get(serve_id)
    return render_template("user/serve_detail.html", serve=serve)


# search serve
@bp.route("/search_serve")
def search_serve():
    query = request.args.get("query")
    serves = ServeModel.query.filter(or_(ServeModel.servename.contains(query),
                                         ServeModel.classification.contains(query),
                                         ServeModel.obj.contains(query),
                                         ServeModel.price.contains(query), ))

    return render_template("user/serve.html", serves=serves)


# user table
@bp.route("/adm/user")
def adm_user():
    users = UserModel.query.all()
    return render_template("adm/adm-user.html", users=users)


# user edit
@bp.route("/adm/user_edit/<int:user_id>", methods=['GET', 'POST'])
def user_edit(user_id):
    user = UserModel.query.get(user_id)
    if request.method == 'GET':
        return render_template("adm/user_edit.html", user=user)
    else:
        form = Edit_User_Form(request.form)
        if form.validate():
            user.username = form.username.data
            user.email = form.email.data
            user.password = form.password.data

            db.session.commit()
            return redirect(url_for("user.adm_user"))
        else:
            flash("The message format is incorrect.")
            return redirect(url_for("user.user_edit", user_id=user_id))


# serve delete
@bp.route("/user_delete/<int:user_id>")
def user_delete(user_id):
    UserModel.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect(url_for("user.adm_user"))


# search
@bp.route("/search_user")
def search_user():
    query = request.args.get("query")
    users = UserModel.query.filter(or_(UserModel.username.contains(query),
                                       UserModel.email.contains(query),
                                       UserModel.password.contains(query), ))

    return render_template("adm/adm-user.html", users=users)


# add user
@bp.route("/add_user", methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template("adm/add_user.html")
    else:
        form = Add_User_Form(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data

            user = UserModel(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.adm_user"))
        else:
            email = form.email.data
            user_model = UserModel.query.filter_by(email=email).first()
            if user_model:
                flash("The email address has been registered.")
            else:
                flash("The message format is incorrect.")
            return redirect(url_for("user.add_user"))


# personal information
@bp.route("/personal_edit/<int:user_id>", methods=['GET', 'POST'])
def personal_edit(user_id):
    user = UserModel.query.get(user_id)
    if request.method == 'GET':
        return render_template("index/personal.html", user=user)
    else:
        form = Edit_User_Form(request.form)
        if form.validate():
            user.username = form.username.data
            user.email = form.email.data
            user.password = form.password.data

            db.session.commit()
            # Clear all data in the session
            session.clear()
            return redirect(url_for("user.sign_in"))
        else:
            flash("The message format is incorrect.")
            return redirect(url_for("user.personal_edit", user_id=user_id))
