from flask import Flask, jsonify
from sqlalchemy.exc import IntegrityError
from errors.auth_errors import InvalidCredentials, NotEnoughRights
from blueprints.event import events
from blueprints.user import users
from blueprints.ticketactions import ticketactions
app = Flask(__name__)
app.register_blueprint(events)
app.register_blueprint(users)
app.register_blueprint(ticketactions)


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


