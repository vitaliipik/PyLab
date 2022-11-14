from flask import Flask
from sqlalchemy.exc import IntegrityError

from blueprints.event import events
from blueprints.user import users
from blueprints.ticketactions import ticketactions
app = Flask(__name__)
app.register_blueprint(events)
app.register_blueprint(users)
app.register_blueprint(ticketactions)


@app.route("/api/v1/hello-world-21")
def hello_world():
    return "Hello, World 21"


@app.errorhandler(ValueError)
def value_error_handler(e):
    return str(e), 400


@app.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return str(e), 400


@app.errorhandler(Exception)
def base_error_handler(e):
    return str(e), 400
