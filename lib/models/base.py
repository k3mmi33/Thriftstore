from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create database engine
engine = create_engine('sqlite:///thrift_store.db', echo=False)

# Create base class for all models
Base = declarative_base()

# Create session factory
Session = sessionmaker(bind=engine)

def get_session():
    """Get a new database session"""
    return Session()

def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(engine)