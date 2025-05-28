from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
import datetime
from db.base import Base

class Lease(Base):
    __tablename__ = 'leases'
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    property_id = Column(Integer, ForeignKey('properties.id'))
    start_date = Column(Date, default=datetime.date.today)
    duration_months = Column(Integer, nullable=False)

    tenant = relationship("Tenant", back_populates="leases")
    property = relationship("Property", back_populates="leases")

    def __repr__(self):
        return f"Lease(id={self.id}, tenant={self.tenant.name}, property={self.property.address},start_date={self.start_date}, duration_months={self.duration_months})"
