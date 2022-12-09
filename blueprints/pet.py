from flask import Blueprint, render_template, request, redirect, url_for, flash
from exts import db
from model import UserModel, ServeModel, PetModel, PASModel
from .form import Pet_Form, PAS_Form
from config import logger
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
            logger.info(f'Add pet: {petname} for {masteremail} successfully.')
            return redirect(url_for("pet.adm_pet"))
        else:
            flash("The message format is incorrect.")
            logger.warning(f'The message format is incorrect, add pet failed.')
            return redirect(url_for("pet.pet_add"))


# pet detail
@bp.route("/pet_detial/<int:pet_id>")
def pet_detail(pet_id):
    pet = PetModel.query.get(pet_id)
    panss = PASModel.query.filter_by(petid = pet_id)
    return render_template("adm/pet_detail.html", pet=pet,panss=panss)


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
            logger.info(f'Edit pet: {pet.petname} for {masteremail} successfully.')
            return redirect(url_for("pet.adm_pet"))
        else:
            flash("The message format is incorrect.")
            logger.warning(f'The message format is incorrect, edit pet: {pet.petname} failed.')
            return redirect(url_for("pet.pet_edit", pet_id=pet_id))


# pet delete
@bp.route("/pet_delete/<int:pet_id>")
def pet_delete(pet_id):
    pet = PetModel.query.filter_by(id=pet_id).first()
    PetModel.query.filter_by(id=pet_id).delete()
    db.session.commit()
    logger.info(f'Delete pet: {pet.petname} successfully.')
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
@bp.route("/<int:user_id>/user_edit_pet/<int:pet_id>", methods=['GET', 'POST'])
def user_edit_pet(pet_id,user_id):
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
            logger.info(f'{user_id} edit pet: {pet.petname} successfully.')
            return redirect(url_for("pet.user_pet",user_id = user_id))
        else:
            flash("The message format is incorrect.")
            logger.warning(f'The message format is incorrect,{user_id} edit pet: {pet.petname} failed.')
            return redirect(url_for("pet.user_edit_pet", pet_id=pet_id))

# user pet delete
@bp.route("/<int:user_id>/user_pet_delete/<int:pet_id>")
def user_pet_delete(pet_id,user_id):
    user = UserModel.query.filter_by(id=user_id).first()
    pet = PetModel.query.filter_by(id=pet_id).first()
    PetModel.query.filter_by(id=pet_id).delete()
    db.session.commit()
    logger.info(f'{user.email} delete pet: {pet.petname} successfully.')
    return redirect(url_for("pet.user_pet",user_id = user_id))

# user add pet
@bp.route("/<int:user_id>/user_add_pet", methods=['GET', 'POST'])
def user_add_pet(user_id):
    user = UserModel.query.filter_by(id=user_id).first()
    if request.method == 'GET':
        return render_template("user/add_pet.html")
    else:
        form = Pet_Form(request.form)
        if form.validate():
            masterid = user_id
            petname = form.petname.data
            species = form.species.data
            breed = form.breed.data
            sex = form.sex.data
            birthday = form.birthday.data

            pet = PetModel(masterid=masterid, petname=petname, species=species, breed=breed,
                           sex=sex, birthday=birthday)
            db.session.add(pet)
            db.session.commit()
            logger.info(f'{user.email} add pet: {petname} successfully.')
            return redirect(url_for("pet.user_pet",user_id = user_id))
        else:
            flash("The message format is incorrect.")
            logger.warning(f'The message format is incorrect, {user.email} add pet failed.')
            return redirect(url_for("pet.user_add_pet",user_id = user_id))

# pet add serve
@bp.route("/pet_add_serve/<int:pet_id>",methods=['GET', 'POST'])
def pet_add_serve(pet_id):
    pet = PetModel.query.get(pet_id)
    if request.method == 'GET':
        return render_template("adm/pet_add_serve.html", pet=pet)
    else:
        form = PAS_Form(request.form)
        if form.validate():
            pet.petname = form.petname.data
            servename = form.servename.data
            serve = ServeModel.query.filter_by(servename=servename).first()
            serveid = serve.id
            petid = pet_id

            pas = PASModel(petid=petid, serveid=serveid)
            db.session.add(pas)
            db.session.commit()
            logger.info(f'Add serve: {servename} for pet: {pet.petname} successfully.')
            return redirect(url_for("pet.pet_detail",pet_id = pet_id))
        else:
            flash("The message format is incorrect.")
            logger.warning(f'The message format is incorrect, add serve for pet: {pet.petname} failed.')
            return redirect(url_for("pet.pet_add_serve",pet_id=pet_id))

# pet add serve
@bp.route("/serve_add_pet/<int:serve_id>",methods=['GET', 'POST'])
def serve_add_pet(serve_id):
    serve = ServeModel.query.get(serve_id)
    if request.method == 'GET':
        return render_template("adm/serve_add_pet.html", serve=serve)
    else:
        form = PAS_Form(request.form)
        if form.validate():
            serve.servename = form.servename.data
            petname = form.petname.data
            pet = PetModel.query.filter_by(petname=petname).first()
            serveid = serve_id
            petid = pet.id

            pas = PASModel(petid=petid, serveid=serveid)
            db.session.add(pas)
            db.session.commit()
            logger.info(f'Add serve: {serve.servename} for pet: {petname} successfully.')
            return redirect(url_for("pet.pet_detail",pet_id = pet.id))
        else:
            flash("The message format is incorrect.")
            logger.warning(f'The message format is incorrect, add serve: {serve.servename} for pet failed.')
            return redirect(url_for("pet.pet_add_serve",serve_id=serve_id))

# pet serve delete
@bp.route("/pas_delete/<int:pas_id>")
def pas_delete(pas_id):
    pas = PASModel.query.filter_by(id=pas_id).first()
    pet = PetModel.query.filter_by(id=pas.petid).first()
    serve = PetModel.query.filter_by(id=pas.serveid).first()
    PASModel.query.filter_by(id=pas_id).delete()
    db.session.commit()
    logger.info(f'Delete serve: {serve.servename} for pet: {pet.petname} successfully.')
    return redirect(url_for("pet.pet_detail",pet_id = pas.petid))

# user - pet add serve
@bp.route("/user_serve_add_pet/<int:serve_id>",methods=['GET', 'POST'])
def user_serve_add_pet(serve_id):
    serve = ServeModel.query.get(serve_id)
    if request.method == 'GET':
        return render_template("user/serve_add_pet.html", serve=serve)
    else:
        form = PAS_Form(request.form)
        if form.validate():
            serve.servename = form.servename.data
            petname = form.petname.data
            pet = PetModel.query.filter_by(petname=petname).first()
            serveid = serve_id
            petid = pet.id

            pas = PASModel(petid=petid, serveid=serveid)
            db.session.add(pas)
            db.session.commit()
            logger.info(f'{pet.user.email} add serve: {serve.servename} for pet: {petname} successfully.')
            return redirect(url_for("pet.user_pet_detail",pet_id = pas.petid))
        else:
            flash("The message format is incorrect.")
            logger.warning(f'The message format is incorrect, add serve: {serve.servename} for pet failed.')
            return redirect(url_for("pet.user_serve_add_pet",serve_id=serve_id))

# user - pet detail
@bp.route("/user_pet_detial/<int:pet_id>")
def user_pet_detail(pet_id):
    pet = PetModel.query.get(pet_id)
    panss = PASModel.query.filter_by(petid = pet_id)
    return render_template("user/pet_detail.html", pet=pet,panss=panss)

# user-pet serve delete
@bp.route("/user_pas_delete/<int:pas_id>")
def user_pas_delete(pas_id):
    pas = PASModel.query.filter_by(id=pas_id).first()
    PASModel.query.filter_by(id=pas_id).delete()
    db.session.commit()
    logger.info(f'{pas.pet.user.email} add serve: {pas.serve.servename} for pet: {pas.pet.petname} successfully.')
    return redirect(url_for("pet.user_pet_detail",pet_id = pas.petid))