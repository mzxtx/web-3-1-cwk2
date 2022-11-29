import  wtforms
from wtforms.validators import length,email,EqualTo
from model import UserModel,ServeModel

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