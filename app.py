from flask import Flask
import config
from exts import db
from blueprints import pet_bp
from blueprints import user_bp
from flask_migrate import Migrate

import os


app = Flask(__name__)
# Bind database configuration
app.config.from_object(config)
db.init_app(app)

migrate = Migrate(app,db)

app.register_blueprint(pet_bp)
app.register_blueprint(user_bp)

#set secret key
app.config['SECRET_KEY'] = os.urandom(24)


if __name__ == '__main__':
    app.run()
