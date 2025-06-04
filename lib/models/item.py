from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    cost = Column(Float, default=0.0)
    quantity = Column(Integer, default=1)
    condition = Column(String(50), default='Good')  # New, Excellent, Good, Fair, Poor
    size = Column(String(20))  # For clothing items
    brand = Column(String(100))
    color = Column(String(50))
    is_sold = Column(Boolean, default=False)
    date_added = Column(DateTime, default=datetime.utcnow)
    date_sold = Column(DateTime)

    # Relationships
    sale_items = relationship("SaleItem", back_populates="item")

    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name}', price=KES{self.price})>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'cost': self.cost,
            'quantity': self.quantity,
            'condition': self.condition,
            'size': self.size,
            'brand': self.brand,
            'color': self.color,
            'is_sold': self.is_sold,
            'date_added': self.date_added.strftime('%Y-%m-%d %H:%M') if self.date_added else None,
            'date_sold': self.date_sold.strftime('%Y-%m-%d %H:%M') if self.date_sold else None
        }
