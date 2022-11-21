from flask import Blueprint, request, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from errors.auth_errors import NotEnoughRights
from blueprints.auth import auth
from models.models import Ticket, Event, Role

engine = create_engine("postgresql://postgres:admin@localhost:5432/Booking_Service")
Session = sessionmaker(bind=engine)
ticketactions = Blueprint('ticketactions', __name__)


@ticketactions.route("/api/v1/ticket", methods=['POST'])
@auth.login_required()
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
            ticket.user_id = auth.current_user().id
            event = session.query(Event).filter_by(id=ticket.event_id).first()
            if ticket.seat > event.tickets_count:
                return Response(f"Invalid seat, max is {event.tickets_count}", status=400)
            session.add(ticket)
    except Exception as e:
        return Response(str(e), status=400)
    return Response("Success", status=200)


@ticketactions.route("/api/v1/updateTicket/<identifier>", methods=['PUT'])
@auth.login_required()
def update_ticket(identifier):
    data = request.get_json()
    if 'status' not in data:
        return Response("Status not found in the body", status=400)
    try:
        with Session.begin() as session:
            ticket_query = session.query(Ticket).filter(Ticket.id == identifier)
            ticket = ticket_query.first()
            if ticket.user_id != auth.current_user().id and auth.current_user().role != Role.admin:
                raise NotEnoughRights("You don't have enough rights to update this ticket!")
            updated = ticket_query.update(data, synchronize_session='fetch')
            if updated == 0:
                return Response("Invalid id specified", status=400)
    except BaseException as e:
        return Response(str(e), status=400)
    return Response("Success!", status=200)


@ticketactions.route("/api/v1/cancelTicket/<identifier>", methods=['DELETE'])
@auth.login_required()
def cancel_ticket(identifier):
    with Session.begin() as session:
        ticket_query = session.query(Ticket).filter(Ticket.id == int(identifier))
        ticket = ticket_query.first()
        if ticket.user_id != auth.current_user().id and auth.current_user().role != Role.admin:
            raise NotEnoughRights("You don't have enough rights to cancel this ticket!")
        deleted = ticket_query.delete(synchronize_session="fetch")
        if deleted == 0:
            return Response("Invalid id specified in /api/v1/cancelTicket/<identifier>", status=400)

    return Response(f"Successfully deleted ticket", status=200)
