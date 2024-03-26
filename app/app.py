from flask import Flask
import os

app = Flask(__name__)

app.secret_key = "4083748udfioHH"

UPLOAD_FOLDER = os.path.join('static','uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
