from lib.models.base import get_session
from lib.models.sale import Sale
from lib.models.sale_item import SaleItem
from lib.models.item import Item
from lib.services.item_service import ItemService
from datetime import datetime

class SalesService:

    @staticmethod
    def create_sale(customer_id=None, payment_method='Cash', tax_rate=0.0,
                   discount_amount=0.0, notes=None):
        """Create a new sale"""
        session = get_session()
        try:
            sale = Sale(
                customer_id=customer_id,
                payment_method=payment_method,
                tax_amount=0.0,
                discount_amount=discount_amount,
                notes=notes
            )
            session.add(sale)
            session.commit()
            return sale
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def add_item_to_sale(sale_id, item_id, quantity=1, custom_price=None):
        """Add an item to a sale"""
        session = get_session()
        try:
            # Get the sale and item
            sale = session.query(Sale).filter(Sale.id == sale_id).first()
            item = session.query(Item).filter(Item.id == item_id).first()

            if not sale or not item:
                return None

            # Use custom price if provided, otherwise use item price
            unit_price = custom_price if custom_price is not None else item.price
            total_price = unit_price * quantity

            # Create sale item
            sale_item = SaleItem(
                sale_id=sale_id,
                item_id=item_id,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price
            )

            session.add(sale_item)

            # Update sale total
            sale.total_amount += total_price

            session.commit()
            return sale_item
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def remove_item_from_sale(sale_id, item_id):
        """Remove an item from a sale"""
        session = get_session()
        try:
            sale_item = session.query(SaleItem).filter(
                SaleItem.sale_id == sale_id,
                SaleItem.item_id == item_id
            ).first()

            if sale_item:
                # Update sale total
                sale = session.query(Sale).filter(Sale.id == sale_id).first()
                if sale:
                    sale.total_amount -= sale_item.total_price

                session.delete(sale_item)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def complete_sale(sale_id, tax_rate=0.0):
        """Complete a sale and mark items as sold"""
        session = get_session()
        try:
            sale = session.query(Sale).filter(Sale.id == sale_id).first()
            if not sale:
                return None

            # Calculate tax
            sale.tax_amount = sale.total_amount * tax_rate

            # Mark all items in the sale as sold
            for sale_item in sale.sale_items:
                item = session.query(Item).filter(Item.id == sale_item.item_id).first()
                if item:
                    item.is_sold = True
                    item.date_sold = datetime.utcnow()

            sale.status = 'Completed'
            session.commit()
            return sale
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_all_sales():
        """Get all sales"""
        session = get_session()
        try:
            return session.query(Sale).order_by(Sale.sale_date.desc()).all()
        finally:
            session.close()

    @staticmethod
    def get_sale_by_id(sale_id):
        """Get sale by ID with items"""
        session = get_session()
        try:
            return session.query(Sale).filter(Sale.id == sale_id).first()
        finally:
            session.close()

    @staticmethod
    def get_sales_by_date_range(start_date, end_date):
        """Get sales within a date range"""
        session = get_session()
        try:
            return session.query(Sale).filter(
                Sale.sale_date >= start_date,
                Sale.sale_date <= end_date
            ).all()
        finally:
            session.close()

    @staticmethod
    def get_sales_summary():
        """Get sales summary statistics"""
        session = get_session()
        try:
            from sqlalchemy import func

            # Total sales count and amount
            total_sales = session.query(func.count(Sale.id)).scalar() or 0
            total_revenue = session.query(func.sum(Sale.total_amount + Sale.tax_amount - Sale.discount_amount)).scalar() or 0

            # Today's sales
            today = datetime.now().date()
            today_sales = session.query(func.count(Sale.id)).filter(
                func.date(Sale.sale_date) == today
            ).scalar() or 0

            today_revenue = session.query(
                func.sum(Sale.total_amount + Sale.tax_amount - Sale.discount_amount)
            ).filter(func.date(Sale.sale_date) == today).scalar() or 0

            return {
                'total_sales': total_sales,
                'total_revenue': total_revenue,
                'today_sales': today_sales,
                'today_revenue': today_revenue
            }
        finally:
            session.close()

    @staticmethod
    def cancel_sale(sale_id):
        """Cancel a sale and unmark items as sold"""
        session = get_session()
        try:
            sale = session.query(Sale).filter(Sale.id == sale_id).first()
            if not sale:
                return None

            # Unmark items as sold
            for sale_item in sale.sale_items:
                item = session.query(Item).filter(Item.id == sale_item.item_id).first()
                if item:
                    item.is_sold = False
                    item.date_sold = None

            # Delete the sale
            session.delete(sale)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()