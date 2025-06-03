from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
import datetime
from db.base import Base

class Lease(Base):
    __tablename__ = 'leases'
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
    property_id = Column(Integer, ForeignKey('properties.id'))
    start_date = Column(Date, default=datetime.date.today)
    duration_months = Column(Integer, nullable=False)

    tenant = relationship("Tenant", back_populates="leases")
    property = relationship("Property", back_populates="leases")
    room = relationship("Room", back_populates="lease")
    payments = relationship("Payment", back_populates="lease")


    def __repr__(self):
        return (f"Lease(id={self.id}, "
            f"tenant={self.tenant.name if self.tenant else 'N/A'}, "
            f"property={self.property.address if self.property else 'N/A'}, "
            f"room={self.room.room_number if self.room else 'N/A'}, "
            f"start_date={self.start_date}, "
            f"duration_months={self.duration_months})"
            )
