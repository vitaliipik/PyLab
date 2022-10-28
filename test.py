from models.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine("postgresql://postgres:admin@localhost:5432/Booking_Service")

Base.metadata.create_all(engine)
