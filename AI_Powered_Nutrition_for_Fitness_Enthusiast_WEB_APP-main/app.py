#request-for accessing file which was uploaded by the user on our application.
import os
import tensorflow as tf

import numpy as np  # used for numerical analysis
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

from flask import Flask, render_template, request, url_for
from tensorflow.keras.preprocessing import image
from keras.models import load_model  # to load our trained model

app = Flask(__name__,template_folder="templates") # initializing a flask app
# Loading the model
picturef=os.path.join('static','image')
app.config['UPLOAD_FOLDERS']=picturef
model=load_model('Fruites.h5')
print("Loaded model from disk")


@app.route('/')# route to display the home page
def home():
    pic1=os.path.join(app.config['UPLOAD_FOLDERS'],'logo1.png')
    pic2=os.path.join(app.config['UPLOAD_FOLDERS'],'apple.png')
    pic3=os.path.join(app.config['UPLOAD_FOLDERS'],'orange.png')
    pic4=os.path.join(app.config['UPLOAD_FOLDERS'],'banana.png')
    pic5=os.path.join(app.config['UPLOAD_FOLDERS'],'pineapple.png')
    pic6=os.path.join(app.config['UPLOAD_FOLDERS'],'watermelon.png')

    return render_template('Index.html', image1=pic1,image2=pic2,image3=pic3,image4=pic4,image5=pic5,imagr6=pic6)#rendering the home page

@app.route('/analyser')# routes to the index html
def image1():
    pic1=os.path.join(app.config['UPLOAD_FOLDERS'],'Fruites.jpg')
    return render_template("Analyzer.html",image1=pic1) 

 

@app.route('/ai',methods=['GET', 'POST'])# route to show the predictions in a web UI
def launch():
    pic1=os.path.join(app.config['UPLOAD_FOLDERS'],'Fruites.jpg')
    if request.method=='POST':
        f=request.files['image'] 
        print('current path')#requesting the file
        basepath=os.path.dirname('__file__')
        print('current path',basepath)#storing the file directory
        filepath=os.path.join(basepath,"uploads",f.filename)
        print('upload folder is',filepath)#storing the file in uploads folder
        f.save(filepath)#saving the file
        
        img=image.load_img(filepath,target_size=(64,64)) #load and reshaping the image
        x=image.img_to_array(img)#converting image to an array
        x=np.expand_dims(x,axis=0)#changing the dimensions of the image

       
      
       # pred=model.predict(x)
        pred = np.argmax (model.predict(x))
        print("prediction",pred)#printing the prediction
        index=['APPLES','BANANA','ORANGE','PINEAPPLE','WATERMELON']
        val=index[pred]
        text = 'The predicted Frite is: ' + str(val)
        
        
    
    return render_template('Result.html', showcase1=text , image1=pic1)

if __name__ == "__main__":
   # running the app
    app.run(debug=False)
