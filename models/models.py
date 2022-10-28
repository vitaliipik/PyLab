from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date
from sqlalchemy.orm import declarative_base, relationship
import enum


Base = declarative_base()


class Role(enum.Enum):
    user = 'user'
    admin = 'admin'


class Status1(enum.Enum):
    booked = 'booked'
    bought = 'bought'
    expired = 'expired'


class Event(Base):
    __tablename__ = 'Event'

    id = Column(Integer, primary_key=True)
    address = Column(String)
    date = Column(Date)
    tickets_count = Column(Integer)


class Ticket(Base):
    __tablename__ = 'Ticket'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('Event.id'))
    user_id = Column(Integer, ForeignKey('User.id'))
    seat = Column(Integer)
    status = Column(Enum(Status1))


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    phone = Column(String)
    role = Column(Enum(Role))
