from flask import render_template ,url_for,flash,redirect,request,session
from . import app
from flask_mysqldb import MySQL
from .output import output
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash, check_password_hash

mysql = MySQL(app)


# Login routes

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT username, password FROM users WHERE username = %s", (username))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[1], password_input):
            session['username'] = user[0]
            flash('Login successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

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
            return redirect(url_for('register'))

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

# App routes
  
@app.route('/home',methods=['GET','POST'])
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