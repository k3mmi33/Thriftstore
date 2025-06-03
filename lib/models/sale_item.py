from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    unit_price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Relationships
    sale = relationship("Sale", back_populates="sale_items")
    item = relationship("Item", back_populates="sale_items")

    def __repr__(self):
        return f"<SaleItem(id={self.id}, item_id={self.item_id}, qty={self.quantity}, subtotal=${self.subtotal:.2f})>"

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'sale_id': self.sale_id,
            'item_id': self.item_id,
            'item_name': self.item.name if self.item else None,
            'unit_price': self.unit_price,
            'quantity': self.quantity,
            'subtotal': self.subtotal
        }