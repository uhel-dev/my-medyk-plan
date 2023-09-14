import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_mysqldb import MySQL

from app.mappings.admin_portal import admin_bp
from app.mappings.stripe import stripe_bp
from app.mappings.subscriptions import subscriptions_bp
from .api import services_blueprint, plans_blueprint, users_blueprint
from .mappings import stripe
from .mappings.member_portal.routes import member_bp
from .models import User

load_dotenv()


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Initialization
mysql = MySQL(app)
login_manager = LoginManager(app)
login_manager.login_view = "sign_in"

app.register_blueprint(services_blueprint)
app.register_blueprint(plans_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(subscriptions_bp, url_prefix='/member-portal/subscriptions')
app.register_blueprint(stripe_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(member_bp)

app.config['JWT_SECRET_KEY'] = 'exe'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
jwt = JWTManager(app)

# DEBUGIN EXPOSED PATHS
# for rule in app.url_map.iter_rules():
#     print(rule)


# User Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.get(mysql.connection, user_id)


from app import routes
