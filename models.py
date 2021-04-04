from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from mixins import StatDataMixin
from sqlalchemy import desc

Base = declarative_base()


class User(StatDataMixin, Base):
    __tablename__ = 'user'

    username = Column(String(250), primary_key=True)
    name = Column(String(250), nullable=False)
    total_byte = Column(Integer)

    def get_total_byte(self, session):
        total_byte = 0
        for device in session.query(Device).filter(Device.owner==self).order_by(desc(Device.total_byte)):
            total_byte += device.get_full_total_byte(session)
        return total_byte

    def __repr__(self):
        return f"User({self.__str__()})"

    def __str__(self):
        return f"{self.name}"

class Device(StatDataMixin, Base):
    __tablename__ = 'device'

    mac = Column(String(250), primary_key=True)
    owner_username = Column(Integer, ForeignKey('user.username'))
    owner = relationship(User)
    name = Column(String(250))
    ip_number = Column(String(250))
    total_byte = Column(Integer)

    def __repr__(self):
        return f"Device({self.__str__()})"

    def __str__(self):
        return f"{self.name}"

    def get_full_total_byte(self, session):
        last_data_usage_reading = session.query(DataUsageReading).filter_by(
            device=self
        ).order_by(desc(DataUsageReading.created_date)).first()
        last_total = (
            last_data_usage_reading.total_byte
            if last_data_usage_reading else 0
        )
        device_total = self.total_byte or 0
        total_byte = device_total + last_total
        return total_byte

class DataUsageReading(StatDataMixin, Base):
    __tablename__ = 'data_usage_reading'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.now)
    device_mac = Column(Integer, ForeignKey('device.mac'))
    device = relationship(Device)
    total_byte = Column(Integer)

    def __repr__(self):
        return f"DataUsageReading({self.__str__()})"

    def __str__(self):
        return f"{self.created_date.strftime('%D %T')} | {self.device.name}: {self.total_best_unit}"



