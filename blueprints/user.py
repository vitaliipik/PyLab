from flask import Blueprint, jsonify
from sqlalchemy import create_engine
import bcrypt
import base64
from sqlalchemy.exc import IntegrityError
from flask import request
from sqlalchemy.orm import sessionmaker

from blueprints.auth import auth
from errors.auth_errors import NotEnoughRights, InvalidCredentials
from models.models import Ticket, User, Role
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
                token = base64.encodebytes(f"{data['email']}:{data['password']}".encode('utf-8'))
                return jsonify({'basic': token.decode("utf-8").replace("\n", "")}), 200
    except IntegrityError:
        raise InvalidCredentials("A password or username is wrong. Try again.")
    return Response("Invalid request body, specify password and username, please!", status=400)


@users.route("/api/v1/user/<username>", methods=['GET'])
def get_user(username: str):
    with Session.begin() as session:
        user = session.query(User).filter_by(username=username).first()
        if user is None:
            return Response("No such user exists", status=404)

        return Response(json.dumps(user.to_dict()), status=200)


@users.route("/api/v1/user", methods=['PUT'])
@auth.login_required()
def update_user():
    data = request.get_json()
    if data is None:
        return Response("No JSON data has been specified!", status=400)
    with Session.begin() as session:
        if auth.current_user().role != Role.admin and \
                'username' in data and \
                auth.current_user().username != data['username']:
            raise NotEnoughRights("Not enough rights to update user")
        user = User(**data) # check if it validates
        if 'password' in data:
            data['password'] = user.password
        session.query(User).filter(User.username == user.username).update(data,
                                                                    synchronize_session="fetch")
    return Response("Success my man!", status=200)


@users.route("/api/v1/user/<username>", methods=['DELETE'])
@auth.login_required()
def delete_user(username):
    role = auth.current_user().role
    if Role.admin != role:
        raise NotEnoughRights("Not enough rights to delete user")
    with Session.begin() as session:
        users_deleted = session.query(User).filter(User.username == username).delete(synchronize_session="fetch")
        if users_deleted == 0:
            return Response("Id was wrong", status=400)

        return Response("Success!", status=200)


@users.route("/api/v1/user/<username>/tickets", methods=['GET'])
@auth.login_required()
def get_user_tickets(username):
    if auth.current_user().role != Role.admin and \
            auth.current_user().username != username:
        raise NotEnoughRights("Not enough rights to get user by this username")
    with Session.begin() as session:
        if session.query(User).filter(User.username == username).first() is None:
            return Response(status=400)
        entries = session.query(Ticket).filter(User.username == username).join(User, User.id == Ticket.user_id)
        tickets = [i.to_dict() for i in entries]

        return Response(json.dumps(tickets), status=200)
