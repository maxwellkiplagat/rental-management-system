from sqlalchemy import Column, Integer, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
import datetime
from db.base import Base

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    lease_id = Column(Integer, ForeignKey('leases.id'))
    amount = Column(Float, nullable=False)
    payment_date = Column(Date, default=datetime.date.today)

    lease = relationship("Lease", back_populates="payments")

    def __repr__(self):
        return f"Payment(id={self.id}, lease_id={self.lease_id}, amount={self.amount}, date={self.payment_date})"
