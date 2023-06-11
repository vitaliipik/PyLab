from flask import Blueprint
from sqlalchemy import create_engine
from blueprints.auth import auth
from sqlalchemy.exc import IntegrityError
from flask import request
from sqlalchemy.orm import sessionmaker

from models.models import Event
from flask import Response
import json

engine = create_engine("postgresql://postgres:admin@localhost:5432/Booking_Service")
Session = sessionmaker(bind=engine)
events = Blueprint('events', __name__)


@events.route("/api/v1/event", methods=['POST'])
@auth.login_required(role='admin')
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
    return {"message":"Successes", "status_code":200},200


@events.route("/api/v1/event", methods=['GET'])
def get_event():
    param = request.args

    if not len(param):
        with Session.begin() as session:
            events = session \
                .query(Event)
            allEvents = [i.to_dict() for i in events]
            if events is None:
                return {"message": "No entry has been found", "status_code": 404}, 404

            return Response(json.dumps(allEvents), status=200)

    if 'event' not in param:
        return {"message":"No event name specified in the query params", "status_code":400},400
    with Session.begin() as session:
        event = session \
            .query(Event).filter(Event.name == param.get('event')).first()

        if event is None:
            return {"message":"No entry has been found", "status_code":404},404

        return Response(json.dumps(event.to_dict()), status=200)


@events.route("/api/v1/event/<int:event_id>", methods=['GET'])
def event_by_id(event_id):
    with Session.begin() as session:
        event = session.query(Event)
        currentEvent = event.get(event_id)
        if currentEvent is None:
            return Response(status=404)
        currentEvent = json.dumps(currentEvent.to_dict())
        return Response(currentEvent, status=200, mimetype="application/json")


@events.route("/api/v1/event/seat/<int:event_id>", methods=['GET'])
def event_seat_by_id(event_id):
    with Session.begin() as session:
        event = session.query(Event)
        currentEvent = event.get(event_id)
        if currentEvent is None:
            return Response(status=404)
        allSeat=[ i+1 for i in range(currentEvent.tickets_count)]
        allReservedSeat=[i.seat for i in currentEvent.tickets]
        for i in allReservedSeat:
            allSeat[i-1]=-1
        allSeat = json.dumps(allSeat)
        return Response(allSeat, status=200, mimetype="application/json")


@events.route("/api/v1/event", methods=['PUT'])
@auth.login_required(role='admin')
def update_event():
    event_data = request.get_json()
    if event_data is None:
        return {"message":"Empty json data has been passed!", "status_code":400},400

    if 'id' not in event_data:
        return {"message":"No id of event has been passed, "
                        "no way we can figure out what's the event we are trying to change", "status_code":400},400
    try:
        with Session.begin() as session:
            event = Event(**event_data)
            updated = session.query(Event).filter(Event.id == event.id).update(event_data,
                                                                               synchronize_session="fetch")
    except:
        return {"message":"Invalid input", "status_code":400},400

    return {"message":"Successes", "status_code":200},200


@events.route("/api/v1/event/<event_id>", methods=["DELETE"])
@auth.login_required(role='admin')
def delete_event(event_id):
    try:
        with Session.begin() as session:
            event = session.query(Event).filter(Event.id == int(event_id)).first()

            if event is None:
                return Response("Id was wrong", status=400)

            session.delete(event)

            return {"message":"Successes", "status_code":200},200
    except:
        return Response("Something went wrong(the id of the event might be wrong) ", status=400)
