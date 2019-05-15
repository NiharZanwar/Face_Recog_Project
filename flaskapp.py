import os
from flask import Flask, render_template, request
#from datetime import datetime
import time


#def generateTimeDate(camera_id):
 #   current_DT=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #current_DT=current_DT.replace('-','')
    #current_DT=current_DT.replace(':','')
  #  current_DT=current_DT.replace(' ','_')
   # return((current_DT+'_'+camera_id))


app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('imageDump')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    #f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    #file.filename=generateTimeDate('3')+'.jpg'
    
    file.filename=(str(int((time.time())*1000000)))+'.jpg'    #convert format from float to int to string
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    file.save(f)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host= '10.42.0.1',debug=True, port=5002)
