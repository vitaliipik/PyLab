from flask import Blueprint, request, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Ticket, Event

engine = create_engine("postgresql://postgres:admin@localhost:5432/Booking_Service")
Session = sessionmaker(bind=engine)
ticketactions = Blueprint('ticketactions', __name__)


@ticketactions.route("/api/v1/ticket", methods=['POST'])
def create_ticket():
    data = request.get_json()

    if data is None:
        return Response("Empty json data", status=400)

    if 'id' in data:
        return Response("Don't specify id in the body", status=400)
    try:

        with Session.begin() as session:
            if not ('event_id' in data and 'seat' in data):
                return Response("No event_id or seat specified")
            if session.query(Ticket.id).filter_by(event_id=data['event_id'], seat=data['seat']).first() is not None:
                return Response("Invalid query(ticket with the same seat already exists)", status=400)
            ticket = Ticket(**data)
            event = session.query(Event).filter_by(id=ticket.event_id).first()
            if ticket.seat > event.tickets_count:
                return Response(f"Invalid seat, max is {event.tickets_count}", status=400)
            session.add(ticket)
    except Exception as e:
        return Response(str(e), status=400)
    return Response("Success", status=200)



@ticketactions.route("/api/v1/updateTicket/<identifier>")
def update_ticket(identifier):
    data = request.get_json()
    if 'status' not in data:
        return Response("Status not found in the body", status=400)
    try:
        with Session.begin() as session:
            updated = session.query(Ticket).filter(Ticket.id == identifier).update({'status': data['status']},
                                                                          synchronize_session="fetch")
            if updated == 0:
                return Response("Invalid id specified", status=400)
    except BaseException as e:
        return Response(str(e), status=400)
    return Response("Success!", status=200)


@ticketactions.route("/api/v1/cancelTicket/<identifier>", methods=['DELETE'])
def cancel_ticket(identifier):
    with Session.begin() as session:
        deleted = session.query(Ticket).filter(Ticket.id == int(identifier)).delete(synchronize_session="fetch")
        if deleted == 0:
            return Response("Invalid id specified in /api/v1/cancelTicket/<identifier>", status=400)

    return Response(f"Successfully deleted ticket", status=200)
