import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

DNS = "postgresql://postgres:postgres@localhost:5432/netology_db"
engine = sqlalchemy.create_engine(DNS)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open("fixtures/tests_data.json", "r") as f:
    data = json.load(f)

for record in data:
    model = {
        "publisher": Publisher,
        "shop": Shop,
        "book": Book,
        "stock": Stock,
        "sale": Sale,
    }[record.get("model")]
    session.add(model(id=record.get("pk"), **record.get("fields")))
session.commit()

publisher_id = None
publisher_name = None
user_input = input("Enter publisher name or id: ")
try:
    publisher_id = int(user_input)
except ValueError:
    publisher_name = user_input

for shop in (
    session.query(Shop)
    .join(Stock.shop)
    .join(Stock.books)
    .join(Book.publisher)
    .filter(Publisher.name.ilike(f"{publisher_name}") | (Publisher.id == publisher_id))
    .all()
):
    print(shop)


# result = (
#     session.query(Publisher)
#     .filter(
#         (Publisher.name.ilike(f"{publisher_name}") | (Publisher.id == publisher_id))
#     )
#     .first()
# )
# print(result)

# for item in session.query(Publisher).filter(Publisher.name.ilike(f"{publisher}")).all():
#     print(item)
# publisher1 = Publisher(name="Vega")
# publisher2 = Publisher(name="Izdanie")
#
# session.add(publisher1)
# session.add(publisher2)
# session.commit()
#
# print(publisher1.id, publisher1.name)
# print(publisher2.id, publisher2.name)
# print(publisher1)
#
# book1 = Book(title="Book1", publisher_id=1)
# book2 = Book(title="Book2", publisher_id=2)
# book3 = Book(title="Book3", publisher_id=1)
# session.add_all([book1, book2, book3])
# session.commit()
#
# for book in session.query(Book).all():
#     print(book)

session.close()
