from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    room_number = Column(String, nullable=False)
    is_occupied = Column(Boolean, default=False)

    property_id = Column(Integer, ForeignKey('properties.id'), nullable=False)
    property = relationship("Property", back_populates="rooms")

    lease = relationship("Lease", back_populates="room", uselist=False)

    def __repr__(self):
        status = "Occupied" if self.is_occupied else "Vacant"
        return f"Room(id={self.id}, number={self.room_number}, status={status}, property_id={self.property_id})"
