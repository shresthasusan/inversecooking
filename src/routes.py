from flask import render_template ,url_for,flash,redirect,request
from . import app
from .output import output
from werkzeug.utils import secure_filename
import os


@app.route('/',methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/about',methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/',methods=['POST','GET'])
def predict():
    imagefile=request.files['imagefile']
    filename = secure_filename(imagefile.filename)
    # image_path=os.path.join(app.root_path,'static\\images\\demo_imgs',imagefile.filename)
    # image_path = os.path.join(app.root_path, 'static', 'images', 'demo_imgs', filename)
    # imagefile.save(image_path)
    # img="/images/demo_imgs/"+imagefile.filename
    title,ingredients,recipe = output(imagefile)
    return render_template('predict.html',title=title,ingredients=ingredients,recipe=recipe,img=imagefile)

@app.route('/<samplefoodname>')
def predictsample(samplefoodname):
    imagefile=os.path.join(app.root_path,'static\\images',str(samplefoodname)+".jpg")
    img="/images/"+str(samplefoodname)+".jpg"
    title,ingredients,recipe = output(imagefile)
    return render_template('predict.html',title=title,ingredients=ingredients,recipe=recipe,img=img)