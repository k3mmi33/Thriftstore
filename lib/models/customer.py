from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True)
    phone = Column(String(20))
    address = Column(Text)
    city = Column(String(100))
    postal_code = Column(String(20))
    date_joined = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)

    # Relationships
    sales = relationship("Sale", back_populates="customer")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.full_name}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'postal_code': self.postal_code,
            'date_joined': self.date_joined.strftime('%Y-%m-%d') if self.date_joined else None,
            'notes': self.notes
        }
