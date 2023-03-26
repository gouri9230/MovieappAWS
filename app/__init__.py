from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

# Creating the app configurations
app.config["SECRET_KEY"] = "fjklajgrighrueia"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://admin:admin123@flaskmoviedb.chhvxuiu6jdh.us-east-1.rds.amazonaws.com/movieapp'

db = SQLAlchemy(app)

login_manager = LoginManager()

# prefix the endpoint with the blueprint name where it is located
login_manager.login_view = "auth.login" 

# Initializing flask extensions
#db.init_app(application)
login_manager.init_app(app)

from app.authentication import auth
from app.movie import mov

#Register blueprints
app.register_blueprint(auth)
app.register_blueprint(mov, url_prefix="/mov")

#optional: to printout the url path of each endpoint
print(app.url_map)

# with application.app_context():
#     db.create_all()

