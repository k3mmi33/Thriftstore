from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    sale_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, nullable=False, default=0.0)
    tax_amount = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    payment_method = Column(String(50), default='Cash')  # Cash, Card, Check
    status = Column(String(20), default='Completed')  # Pending, Completed, Refunded
    notes = Column(Text)

    # Relationships
    customer = relationship("Customer", back_populates="sales")
    sale_items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")

    @property
    def final_total(self):
        return self.total_amount + self.tax_amount - self.discount_amount

    def __repr__(self):
        return f"<Sale(id={self.id}, total=KES{self.final_total}, date='{self.sale_date}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'customer_name': self.customer.full_name if self.customer else 'Walk-in',
            'sale_date': self.sale_date.strftime('%Y-%m-%d %H:%M') if self.sale_date else None,
            'total_amount': self.total_amount,
            'tax_amount': self.tax_amount,
            'discount_amount': self.discount_amount,
            'final_total': self.final_total,
            'payment_method': self.payment_method,
            'status': self.status,
            'notes': self.notes,
            'items_count': len(self.sale_items)
        }
