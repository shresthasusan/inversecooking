from flask import Flask, session
from flask_mysqldb import MySQL
import secrets

app = Flask(__name__,template_folder='Templates')

mysql = MySQL(app)
#mySQL Configuration
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'recipelens'



from . import routes