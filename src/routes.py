from flask import render_template ,url_for,flash,redirect,request,session
from . import app
from flask_mysqldb import MySQL
import MySQLdb.cursors
from .output import output
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,  UserMixin

mysql = MySQL(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin):
    def __init__(self, uid, username, password):
        self.id = uid
        self.username = username
        self.password = password

@app.route("/")
@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        flash('You are already logged in', 'info')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
            username = request.form['username']
            password_input = request.form['password']

            cur = mysql.connection.cursor()
            cur.execute("SELECT uid, username, password FROM users WHERE username = %s", (username,))
            user_data = cur.fetchone()
            cur.close()
            if user_data and check_password_hash(user_data[2], password_input):
                user = User(uid=user_data[0], username=user_data[1], password=user_data[2])
                login_user(user)
                flash('Login successful', 'success')
                return redirect(url_for('home'))  # Redirect to the home route after successful login
            else:
                flash('Invalid username or password', 'error')
                return redirect(url_for('login'))
     
    return render_template('login.html')




@login_manager.user_loader
def load_user(uid):
    cur = mysql.connection.cursor()
    cur.execute("SELECT uid, username, password FROM users WHERE uid = %s", (uid,))
    user_data = cur.fetchone()
    cur.close()

    if user_data:
        return User(uid=user_data[0], username=user_data[1], password=user_data[2])


# Registration Routes

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cur.fetchone()
        cur.close()

        if existing_user:
            flash('Username already exists. Please choose another username.', 'error')
            return render_template('registration.html',error='Invalid username or password')

        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method='sha256')

        # Save 'username' and 'hashed_password' in the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('registration.html')

# Log our route 
@app.route('/logout')
def logout():
    logout_user()
    # Clear the session
    session.clear()

    # Redirect to the login page
    flash('Logout successful', 'success')
    return redirect(url_for('login'))

# App routes
  
@app.route('/home')
@login_required
def home():
    return render_template('home.html')
    

    
@app.route('/about',methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/predict',methods=['POST','GET'])

def predict():
    imagefile = request.files['imagefile']
    filename = secure_filename(imagefile.filename)
    image_path = os.path.join(app.root_path, 'static', 'demo_imgs', filename)
    imagefile.save(image_path)

    img = "/demo_imgs/" + filename
    title, ingredients, recipe = output(image_path)

    return render_template('predict.html', title=title, ingredients=ingredients, recipe=recipe, img=img)

@app.route('/<samplefoodname>')
def predictsample(samplefoodname):
    imagefile=os.path.join(app.root_path,'static\\images',str(samplefoodname)+".jpg")
    img="/images/"+str(samplefoodname)+".jpg"
    title,ingredients,recipe = output(imagefile)
    return render_template('predict.html',title=title,ingredients=ingredients,recipe=recipe,img=img)