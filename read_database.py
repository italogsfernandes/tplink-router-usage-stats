from models import Base, User, Device, DataUsageReading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

print("#"*80)
print("# Valores no banco de dados:")
print("#"*80)
for device in session.query(Device).order_by(desc(Device.total_byte)):
    total_byte = device.get_full_total_byte(session)
    total_device = device.get_total_best_unit(total_byte)
    print(f"{device} | {total_device}")
print("#"*80)
