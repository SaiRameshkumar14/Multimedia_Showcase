from flask import flash, request, redirect, url_for, render_template, Response
import os
import cv2
import urllib.request
from app import app
from app import allowed_file
from werkzeug.utils import secure_filename

#image--------------------------------------------------------------------------------

@app.route('/image')
def upload_form():
    return render_template('image.html')

@app.route('/image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('image.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


img = os.path.join('static', 'image')


#video---------------------------------------------------------------------------------

VIDEO_FOLDER = 'static/video'
app.config['VIDEO_FOLDER'] = VIDEO_FOLDER

@app.route('/video')
def index():
    return render_template('video.html', uploaded_video=None)

@app.route('/video', methods=['POST'])  # Updated route to '/video'
def upload_video():
    if 'video' in request.files:
        video = request.files['video']
        if video.filename != '':
            video_path = os.path.join(app.config['VIDEO_FOLDER'], video.filename)
            video.save(video_path)
            return render_template('video.html', uploaded_video='video/' + video.filename)
    return redirect(url_for('video'))

#webcam---------------------------------------------------------------------------------

camera = cv2.VideoCapture(0)  # 0 corresponds to the default camera (usually the built-in webcam)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
@app.route('/webcam')
def webcam():
    return render_template('webcam.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



#analusis-----------------------------------------------------------------------------------

@app.route('/analysis')
def analysis():
    file = os.path.join(img, 'Default.jpeg')
    return render_template('./analysis.html', image=file)

@app.route('/')
@app.route('/home')
def home():
    return render_template('./home.html')


if __name__ =='__main__':
    app.run(debug=True)