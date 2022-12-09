import sys
sys.path = ['', '..'] + sys.path[1:]
from sqlalchemy import create_engine
from models.models import *
from alembic.config import Config
from alembic import command


engine = create_engine("postgresql://postgres:admin@localhost:5432/Booking_Service")
Base.metadata.create_all(engine)
alembic_cfg = Config("alembic.ini")
command.stamp(alembic_cfg, "head")
