from flask import Blueprint
from sqlalchemy import create_engine
import bcrypt
from sqlalchemy.exc import IntegrityError
from flask import request
from sqlalchemy.orm import sessionmaker

from models.models import Ticket, User
from flask import Response
from models.json_encoder import AlchemyEncoder
import json

engine = create_engine("postgresql://postgres:admin@localhost:5432/Booking_Service")
Session = sessionmaker(bind=engine)
users = Blueprint('user', __name__)


@users.route("/api/v1/user", methods=['POST'])
def create_user():
    user_data = request.get_json()
    if user_data is None:
        return Response(status=400)
    try:
        user = User(**user_data)
        with Session.begin() as session:
            session.add(user)
        return Response()
    except IntegrityError:
        return Response("Couldn't add a user to the db", status=400)


@users.route("/api/v1/user/login", methods=['GET'])
def login_user():
    data = request.get_json()
    if data is None:
        return Response("No JSON data has been specified!", status=400)
    try:
        if 'password' in data and 'username' in data:
            with Session.begin() as session:
                user = session.query(User).filter_by(username=data['username']).first()
                if not bcrypt.checkpw(data['password'].encode("utf-8"), user.password.encode("utf-8")):
                    return Response("Invalid password or username specified", status=404)

                return Response(json.dumps(user.to_dict()), status=200) # this should return token
    except IntegrityError:
        return Response("Invalid username or password specified", status=400)

    return Response("Invalid request body, specify password and username, please!", status=400)


@users.route("/api/v1/user/<username>", methods=['GET'])
def get_user(username: str):
    with Session.begin() as session:
        user = session.query(User).filter_by(username=username).first()
        if user is None:
            return Response("No such user exists", status=404)

        return Response(json.dumps(user.to_dict()), status=200)


@users.route("/api/v1/user", methods=['PUT'])
def update_user():
    data = request.get_json()
    if data is None:
        return Response("No JSON data has been specified!", status=400)
    with Session.begin() as session:
        user = User(**data) # check if it validates
        if 'password' in data:
            data['password'] = user.password
        session.query(User).filter(User.username == user.username).update(data,
                                                                    synchronize_session="fetch")
    return Response("Success my man!", status=200)


@users.route("/api/v1/user/<username>", methods=['DELETE'])
def delete_user(username):
    with Session.begin() as session:
        users_deleted = session.query(User).filter(User.username == username).delete(synchronize_session="fetch")
        if users_deleted == 0:
            return Response("Id was wrong", status=400)

        return Response("Success!", status=200)


@users.route("/api/v1/user/<username>/tickets", methods=['GET'])
def get_user_tickets(username):
    with Session.begin() as session:
        if session.query(User).filter(User.username == username).first() is None:
            return Response(status=400)
        entries = session.query(Ticket).filter(User.username == username).join(User, User.id == Ticket.user_id)
        tickets = [i.to_dict() for i in entries]

        return Response(json.dumps(tickets), status=200)
