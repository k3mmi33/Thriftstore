from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class SaleItem(Base):
    __tablename__ = 'sale_items'

    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey('sales.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    # Relationships
    sale = relationship("Sale", back_populates="sale_items")
    item = relationship("Item", back_populates="sale_items")

    def __repr__(self):
        return f"<SaleItem(sale_id={self.sale_id}, item_id={self.item_id}, qty={self.quantity})>"

    def to_dict(self):
        return {
            'id': self.id,
            'sale_id': self.sale_id,
            'item_id': self.item_id,
            'item_name': self.item.name if self.item else 'Unknown',
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_price': self.total_price
        }