from lib.models.base import get_session
from lib.models.customer import Customer

class CustomerService:

    @staticmethod
    def create_customer(first_name, last_name, email=None, phone=None,
                       address=None, city=None, postal_code=None, notes=None):
        """Create a new customer"""
        session = get_session()
        try:
            customer = Customer(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                postal_code=postal_code,
                notes=notes
            )
            session.add(customer)
            session.commit()
            return customer
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_all_customers():
        """Get all customers"""
        session = get_session()
        try:
            return session.query(Customer).all()
        finally:
            session.close()

    @staticmethod
    def get_customer_by_id(customer_id):
        """Get customer by ID"""
        session = get_session()
        try:
            return session.query(Customer).filter(Customer.id == customer_id).first()
        finally:
            session.close()

    @staticmethod
    def search_customers(search_term):
        """Search customers by name, email, or phone"""
        session = get_session()
        try:
            return session.query(Customer).filter(
                (Customer.first_name.contains(search_term)) |
                (Customer.last_name.contains(search_term)) |
                (Customer.email.contains(search_term)) |
                (Customer.phone.contains(search_term))
            ).all()
        finally:
            session.close()

    @staticmethod
    def update_customer(customer_id, **kwargs):
        """Update a customer"""
        session = get_session()
        try:
            customer = session.query(Customer).filter(Customer.id == customer_id).first()
            if customer:
                for key, value in kwargs.items():
                    if hasattr(customer, key):
                        setattr(customer, key, value)
                session.commit()
                return customer
            return None
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete_customer(customer_id):
        """Delete a customer"""
        session = get_session()
        try:
            customer = session.query(Customer).filter(Customer.id == customer_id).first()
            if customer:
                session.delete(customer)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_customer_with_sales(customer_id):
        """Get customer with their sales history"""
        session = get_session()
        try:
            from lib.models.sale import Sale
            customer = session.query(Customer).filter(Customer.id == customer_id).first()
            if customer:
                sales = session.query(Sale).filter(Sale.customer_id == customer_id).all()
                return customer, sales
            return None, []
        finally:
            session.close()
