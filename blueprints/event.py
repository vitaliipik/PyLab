from flask import Blueprint
from sqlalchemy import create_engine

from sqlalchemy.exc import IntegrityError
from flask import request
from sqlalchemy.orm import sessionmaker

from models.models import Event
from flask import Response
from models.json_encoder import AlchemyEncoder
import json

engine = create_engine("postgresql://postgres:admin@localhost:5432/Booking_Service")
Session = sessionmaker(bind=engine)
events = Blueprint('events', __name__)


@events.route("/api/v1/event", methods=['POST'])
def create_event():
    event_data = request.get_json()
    if event_data is None:
        return Response(status=400)
    try:
        event = Event(**event_data)
        with Session.begin() as session:
            session.add(event)
    except BaseException as e:
        return Response(str(e), status=400)
    return Response(status=200)


@events.route("/api/v1/event", methods=['GET'])
def get_event():
    param = request.args
    if 'event' not in param:
        return Response("No event name specified in the query params", status=400)
    with Session.begin() as session:
        event = session\
            .query(Event).filter(Event.name == param.get('event')).first()

        if event is None:
            return Response("No entry has been found", status=404)

        return Response(json.dumps(event.to_dict()), status=200)


@events.route("/api/v1/event/<event_id>", methods=['GET'])
def event_by_id(event_id):
    with Session.begin() as session:
        event = session.query(Event)
        currentEvent = event.get(event_id)
        if currentEvent is None:
            return Response(status=404)
        currentEvent = json.dumps(currentEvent.to_dict(), cls=AlchemyEncoder)
        return Response(currentEvent, status=200, mimetype="application/json")


@events.route("/api/v1/event", methods=['PUT'])
def update_event():
    event_data = request.get_json()
    if event_data is None:
        return Response("Empty json data has been passed!", status=400)

    if 'id' not in event_data:
        return Response("No id of event has been passed, "
                        "no way we can figure out what's the event we are trying to change", status=400)
    try:
        with Session.begin() as session:
            event = Event(**event_data)
            updated = session.query(Event).filter(Event.id == event.id).update(event_data,
                                                                        synchronize_session="fetch")
            if updated == 0:
                return Response("Invalid id specified, no entries found to update")
    except IntegrityError:
        return Response("Invalid input", status=400)

    return Response("Success!", status=200)


@events.route("/api/v1/event/<event_id>", methods=["DELETE"])
def delete_event(event_id):
    try:
        with Session.begin() as session:
            event = session.query(Event).filter(Event.id == int(event_id)).first()

            if event is None:
                return Response("Id was wrong", status=400)

            session.delete(event)

            return Response("Good stuff, mate!", status=200, mimetype="application/json")
    except IntegrityError as e:
        return Response("Something went wrong(the id of the event might be wrong) " + str(e), status=400)



