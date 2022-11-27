# login interface
from flask import Blueprint, render_template, request, redirect, url_for, session,flash
from exts import db
from model import UserModel
from .form import Sign_up_Form, Sign_in_Form

bp = Blueprint("user", __name__, url_prefix="/user")


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
            if user and user.password == password:
                session['user_id'] = user.id
                return redirect("/")
            else:
                flash("The email address and password do not match.")
                return redirect(url_for("user.sign_in"))
        else:
            flash("The email or password format is incorrect.")
            return redirect(url_for("user.sign_in"))


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
            return redirect(url_for("user.sign_up"))
