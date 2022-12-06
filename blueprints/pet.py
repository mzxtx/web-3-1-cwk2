from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from exts import db
from model import UserModel, ServeModel, PetModel
from .form import Sign_up_Form, Sign_in_Form, Serve_Form, Pet_Form
from sqlalchemy import or_, and_

bp = Blueprint("pet", __name__, url_prefix="/pet")


# adm pet
@bp.route("/adm/pet")
def adm_pet():
    pets = PetModel.query.all()
    return render_template("adm/adm-pet.html", pets=pets)


# add pet
@bp.route("/adm/pet/add", methods=['GET', 'POST'])
def pet_add():
    if request.method == 'GET':
        return render_template("adm/add_pet.html")
    else:
        form = Pet_Form(request.form)
        if form.validate():
            masteremail = form.email.data
            petname = form.petname.data
            species = form.species.data
            breed = form.breed.data
            sex = form.sex.data
            birthday = form.birthday.data
            master = UserModel.query.filter_by(email=masteremail).first()
            masterid = master.id

            pet = PetModel(masterid=masterid, petname=petname, species=species, breed=breed,
                           sex=sex, birthday=birthday)
            db.session.add(pet)
            db.session.commit()
            return redirect(url_for("pet.adm_pet"))
        else:
            flash("The message format is incorrect.")
            return redirect(url_for("pet.pet_add"))


# pet detail
@bp.route("/pet_detial/<int:pet_id>")
def pet_detail(pet_id):
    pet = PetModel.query.get(pet_id)
    return render_template("adm/pet_detail.html", pet=pet)


# pet edit
@bp.route("/pet_edit/<int:pet_id>", methods=['GET', 'POST'])
def pet_edit(pet_id):
    pet = PetModel.query.get(pet_id)
    if request.method == 'GET':
        return render_template("adm/pet_edit.html", pet=pet)
    else:
        form = Pet_Form(request.form)
        if form.validate():
            masteremail = form.email.data
            pet.petname = form.petname.data
            pet.species = form.species.data
            pet.breed = form.breed.data
            pet.sex = form.sex.data
            pet.birthday = form.birthday.data
            master = UserModel.query.filter_by(email=masteremail).first()
            pet.masterid = master.id

            db.session.commit()
            return redirect(url_for("pet.adm_pet"))
        else:
            flash("The message format is incorrect.")
            return redirect(url_for("pet.pet_edit", pet_id=pet_id))


# pet delete
@bp.route("/pet_delete/<int:pet_id>")
def pet_delete(pet_id):
    PetModel.query.filter_by(id=pet_id).delete()
    db.session.commit()
    return redirect(url_for("pet.adm_pet"))


# search pet
@bp.route("/search_pet")
def search_pet():
    query = request.args.get("query")
    pets = PetModel.query.filter(or_(PetModel.petname.contains(query),
                                     # PetModel.user.email.contains(query),
                                     PetModel.species.contains(query),
                                     PetModel.breed.contains(query),
                                     PetModel.sex.contains(query),
                                     PetModel.birthday.contains(query), ))
    return render_template("adm/adm-pet.html", pets=pets)

# search cat
@bp.route("/search_cat")
def search_cat():
    query = request.args.get("query")
    pets = PetModel.query.filter(and_(PetModel.species=='Cat',
                                     PetModel.sex==query))
    return render_template("adm/adm-pet.html", pets=pets)
# search dog
@bp.route("/search_dog")
def search_dog():
    query = request.args.get("query")
    pets = PetModel.query.filter(and_(PetModel.species == 'Dog',
                                      PetModel.sex == query))
    return render_template("adm/adm-pet.html", pets=pets)

# user pet
@bp.route("/user_pet/<int:user_id>")
def user_pet(user_id):
    pets = PetModel.query.filter_by(masterid = user_id)
    return render_template("user/pet.html", pets=pets)

# user edit pet
@bp.route("/user_edit_pet/<int:pet_id>", methods=['GET', 'POST'])
def user_edit_pet(pet_id):
    pet = PetModel.query.get(pet_id)
    if request.method == 'GET':
        return render_template("user/pet_edit.html", pet=pet)
    else:
        form = Pet_Form(request.form)
        if form.validate():
            masteremail = form.email.data
            pet.petname = form.petname.data
            pet.species = form.species.data
            pet.breed = form.breed.data
            pet.sex = form.sex.data
            pet.birthday = form.birthday.data
            master = UserModel.query.filter_by(email=masteremail).first()
            pet.masterid = master.id

            db.session.commit()
            return redirect(url_for("pet.user_pet"))
        else:
            flash("The message format is incorrect.")
            return redirect(url_for("pet.user_edit_pet", pet_id=pet_id))

# user pet delete
@bp.route("/user_pet_delete/<int:pet_id>")
def user_pet_delete(pet_id):
    PetModel.query.filter_by(id=pet_id).delete()
    db.session.commit()
    return redirect(url_for("pet.user_pet"))