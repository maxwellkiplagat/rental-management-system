from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from db.base import Base

class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    rent = Column(Float, nullable=False)

    leases = relationship("Lease", back_populates="property")

    def __repr__(self):
        return f"Property(id={self.id}, address={self.address})"