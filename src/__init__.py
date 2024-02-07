from flask import Flask, session
from flask_mysqldb import MySQL
import secrets
from flask_login import LoginManager,  UserMixin



app = Flask(__name__,template_folder='Templates')
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mysql = MySQL(app)
#mySQL Configuration
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'recipe_user'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'recipelens'








from . import routes