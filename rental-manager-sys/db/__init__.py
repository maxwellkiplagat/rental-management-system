from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base

engine = create_engine('sqlite:///rental.db')
Session = sessionmaker(bind=engine)
session = Session()