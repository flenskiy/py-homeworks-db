import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

DNS = "postgresql://postgres:postgres@localhost:5432/netology_db"
engine = sqlalchemy.create_engine(DNS)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

publisher1 = Publisher(name="Vega")
publisher2 = Publisher(name="Izdanie")

session.add(publisher1)
session.add(publisher2)
session.commit()

print(publisher1.id, publisher1.name)
print(publisher2.id, publisher2.name)

session.close()
