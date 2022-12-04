from flask import Flask,session,g
import config
from exts import db
from blueprints import index_bp,user_bp,serve_bp
from flask_migrate import Migrate
from model import UserModel
import os


app = Flask(__name__)
# Bind database configuration
app.config.from_object(config)
db.init_app(app)

migrate = Migrate(app,db)

app.register_blueprint(index_bp)
app.register_blueprint(user_bp)
app.register_blueprint(serve_bp)

# hook function
@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            #Bind g to a variable called "user" whose value is the user variable
            # setattr(g,"user",user)
            g.user = user
        except:
            g.user = None

# Context processor
@app.context_processor
def context_processor():
    if hasattr(g,"user"):
        return {"user":g.user}
    else:
        return {}

#set secret key
app.config['SECRET_KEY'] = os.urandom(24)


if __name__ == '__main__':
    app.run()
