from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Slot(Base):
    __tablename__ = "slots"
    id = Column(Integer, primary_key=True)
    number = Column(String, unique=True, nullable=False)
    status = Column(String, default="Free")  # Free / Occupied

    vehicles = relationship("Vehicle", back_populates="slot")

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True)
    plate_number = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    slot_id = Column(Integer, ForeignKey("slots.id"))
    checked_in = Column(Boolean, default=False)

    slot = relationship("Slot", back_populates="vehicles")
