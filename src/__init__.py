from flask import Flask
from flask_mysqldb import MySQL
import secrets

app = Flask(__name__,template_folder='Templates')

#mySQL Configuration
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'recipelens'
app.config['MYSQL_USER'] = 'recipe_user'

mysql = MySQL(app)

from . import routes