from datetime import date
from models.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine("postgresql://postgres:admin@localhost:5432/Booking_Service")
Session = sessionmaker(bind=engine)
session = Session()

Event = Event(address='Stryyska',
              date=date(2022, 10, 10),
              tickets_count=110)
User = User(username='seniorohar',
            first_name='Arsenii',
            last_name='Ohar',
            email='arsen.ogar@gmail.com',
            password='neskazhuparolnikolu228',
            phone='380987669293',
            role=Role.admin)
session.add(Event)
session.add(User)
session.commit()
