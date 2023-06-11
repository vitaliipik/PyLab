import re

import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date
from sqlalchemy.orm import declarative_base, relationship, validates
import enum

Base = declarative_base()


class Role(enum.Enum):
    user = 'user'
    admin = 'admin'


class Status1(enum.Enum):
    booked = 'booked'
    bought = 'bought'
    expired = 'expired'

    def __str__(self):
        return str(self.value)


class Event(Base):
    __tablename__ = 'Event'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    date = Column(Date)
    tickets_count = Column(Integer)
    image=Column(String)
    tickets = relationship('Ticket', cascade="all, delete")
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "date": str(self.date),
            "tickets_count": self.tickets_count,
            "image": self.image
        }


class Ticket(Base):
    __tablename__ = 'Ticket'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('Event.id'))
    user_id = Column(Integer, ForeignKey('User.id'))
    seat = Column(Integer)
    status = Column(Enum(Status1))

    event = relationship('Event')

    @validates('seat')
    def validate_seat(self, key, seat):
        if int(seat) <= 0:
            raise ValueError("Incorrect stuff here")
        return int(seat)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "event_id": self.event_id,
            "user_id": self.user_id,
            "seat": self.seat,
            "status": str(self.status)
        }


def validate_name(name):
    length = len(name)
    if length <= 1 or length > 40:
        raise ValueError("Length of name should be less than 40 and more than 4 characters long")
    return name


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    phone = Column(String, unique=True)
    role = Column(Enum(Role))

    tickets = relationship("Ticket", cascade="all, delete")
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "role": str(self.role)
        }

    @validates("username")
    def validate_username(self, key, username):
        length = len(username)
        if length <= 4 or length > 30:
            raise ValueError("Length of username should be less than 30 and more than 5 characters long")
        return username

    @validates("first_name")
    def validate_first_name(self, key, first_name):
        return validate_name(first_name)

    @validates("last_name")
    def validate_last_name(self, key, last_name):
        return validate_name(last_name)

    __email_r = re.compile("""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[""" +
                           """\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")""" +
                           """@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|""" +
                           """2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:""" +
                           """(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")
    __password_r = re.compile("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    __phone_r = re.compile("^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$")

    @validates("email")
    def validate_last_name(self, key, email):
        if User.__email_r.match(email) is None:
            raise ValueError("This is not email")

        return email

    @validates("password")
    def validate_password(self, key, password: str):
        if User.__password_r.match(password) is None:
            raise ValueError("This is not password(8 characters long+, one letter and number")
        password = bytes(password, "utf-8")
        password = bcrypt.hashpw(password, bcrypt.gensalt(12))

        return password.decode("utf-8")

    @validates("phone")
    def validate_phone(self, key, phone):
        if User.__phone_r.match(phone) is None:
            raise ValueError("This is not a phone number")

        return phone



