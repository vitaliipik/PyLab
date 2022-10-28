from datetime import date
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date
from models.models import *
from models.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine("postgresql://postgres:admin@localhost:5432/Booking_Service")
Session = sessionmaker(bind=engine)
session = Session()
Event = Event(address='Stryyska', date=date(2022, 10, 10), tickets_count=110)
session.add(Event)
session.commit()
