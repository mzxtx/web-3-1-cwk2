import  wtforms
from wtforms.validators import length,email,EqualTo,DataRequired
from model import UserModel,ServeModel,PetModel

#Sign in Form
class Sign_in_Form(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])

# Sign up Form
class Sign_up_Form(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=2,max=20)])
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6,max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    # Verify that the email address is registered.
    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError("The email address has been registered.")

#Serve Form
class Serve_Form(wtforms.Form):
    servename = wtforms.StringField(validators=[length(min=2,max=200)])
    classification = wtforms.StringField(validators=[DataRequired()])
    obj = wtforms.StringField(validators=[DataRequired()])
    price = wtforms.FloatField(validators=[DataRequired()])
    introduction = wtforms.StringField(validators=[length(min=0,max=10000)])

# add user form
class Add_User_Form(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=2, max=20)])
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])

    # Verify that the email address is registered.
    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError("The email address has been registered.")

# edit user form
class Edit_User_Form(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=2, max=20)])
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])

# pet form
class Pet_Form(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    petname = wtforms.StringField(validators=[length(min=2, max=20)])
    species = wtforms.StringField(validators=[length(min=2, max=20)])
    breed = wtforms.StringField(validators=[length(min=2, max=20)])
    sex = wtforms.StringField(validators=[length(min=2, max=20)])
    birthday = wtforms.DateField(validators=[DataRequired()])

    # Verify that the email address is existed.
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).count()
        if user == 0:
            raise wtforms.ValidationError("The user does not exist.")

#pas form
class PAS_Form(wtforms.Form):
    petname = wtforms.StringField(validators=[DataRequired()])
    servename = wtforms.StringField(validators=[DataRequired()])
    def validate_servename(self,field):
        servename = field.data
        serve = ServeModel.query.filter_by(servename=servename).count()
        if serve == 0:
            raise wtforms.ValidationError("The serve does not exist.")
    def validate_petname(self, field):
        petname = field.data
        pet = PetModel.query.filter_by(petname=petname).count()
        if pet == 0:
            raise wtforms.ValidationError("The pet does not exist.")