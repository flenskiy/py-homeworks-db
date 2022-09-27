import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

DNS = "postgresql://postgres:postgres@localhost:5432/netology_db"
engine = sqlalchemy.create_engine(DNS)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.close()
