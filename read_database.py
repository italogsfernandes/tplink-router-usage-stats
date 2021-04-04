from models import Base, User, Device, DataUsageReading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from utils import read_and_print_database
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

read_and_print_database(session)