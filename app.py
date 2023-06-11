from flask import  jsonify, Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from errors.auth_errors import InvalidCredentials, NotEnoughRights
from blueprints.event import events
from blueprints.user import users
from blueprints.ticketactions import ticketactions
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)
app.register_blueprint(events)
app.register_blueprint(users)
app.register_blueprint(ticketactions)
app.config['UPLOAD_FOLDER']='static/uploads'


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

@app.route("/")
def hello_world():
    return "Hello, World 21"


@app.errorhandler(ValueError)
def value_error_handler(e):
    return str(e), 400


@app.errorhandler(Exception)
def base_error_handler(e):
    return str(e), 400


@app.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({'message': str(e)}), 400


@app.errorhandler(InvalidCredentials)
def invalid_credentials_handler(e):
    return jsonify({'message': str(e)}), 401


@app.errorhandler(NotEnoughRights)
def invalid_credentials_handler(e):
    return jsonify({'message': str(e),"status_code":403}), 403


@app.errorhandler(Exception)
def base_error_handler(e):
    return str(e), 400


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/v1/upload/file', methods=['POST'])
def upload_image():
	if 'image' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['image']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		return {"message":"Successes my man", "status_code":200},200
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)