from sqlalchemy.orm import Session
from lib.models.base import get_session
from lib.models.item import Item
from datetime import datetime

class ItemService:

    @staticmethod
    def create_item(name, description, category, price, cost=0.0, quantity=1,
                   condition='Good', size=None, brand=None, color=None):
        """Create a new item"""
        session = get_session()
        try:
            item = Item(
                name=name,
                description=description,
                category=category,
                price=price,
                cost=cost,
                quantity=quantity,
                condition=condition,
                size=size,
                brand=brand,
                color=color
            )
            session.add(item)
            session.commit()
            session.refresh(item)
            return item
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_all_items():
        """Get all items"""
        session = get_session()
        try:
            return session.query(Item).all()
        finally:
            session.close()

    @staticmethod
    def get_available_items():
        """Get all available (not sold) items"""
        session = get_session()
        try:
            return session.query(Item).filter(Item.is_sold == False).all()
        finally:
            session.close()

    @staticmethod
    def get_item_by_id(item_id):
        """Get item by ID"""
        session = get_session()
        try:
            return session.query(Item).filter(Item.id == item_id).first()
        finally:
            session.close()

    @staticmethod
    def search_items(search_term):
        """Search items by name, category, or brand"""
        session = get_session()
        try:
            return session.query(Item).filter(
                (Item.name.contains(search_term)) |
                (Item.category.contains(search_term)) |
                (Item.brand.contains(search_term))
            ).all()
        finally:
            session.close()

    @staticmethod
    def update_item(item_id, **kwargs):
        """Update an item"""
        session = get_session()
        try:
            item = session.query(Item).filter(Item.id == item_id).first()
            if item:
                for key, value in kwargs.items():
                    if hasattr(item, key):
                        setattr(item, key, value)
                session.commit()
                session.refresh(item)
                return item
            return None
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete_item(item_id):
        """Delete an item"""
        session = get_session()
        try:
            item = session.query(Item).filter(Item.id == item_id).first()
            if item:
                session.delete(item)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def mark_as_sold(item_id):
        """Mark an item as sold"""
        session = get_session()
        try:
            item = session.query(Item).filter(Item.id == item_id).first()
            if item:
                item.is_sold = True
                item.date_sold = datetime.utcnow()
                session.commit()
                ession.refresh(item)
                return item
            return None
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_categories():
        """Get all unique categories"""
        session = get_session()
        try:
            result = session.query(Item.category).distinct().all()
            return [r[0] for r in result if r[0]]
        finally:
            session.close()