from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///shop.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

    orders = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    orders = relationship("Order", back_populates="product")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    status = Column(Boolean, default=False) 
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")

Base.metadata.create_all(engine)

user1 = User(name="Alice", email="alice@example.com")
user2 = User(name="Bob", email="bob@example.com")

product1 = Product(name="Laptop", price=1200)
product2 = Product(name="Phone", price=800)
product3 = Product(name="Headphones", price=150)

order1 = Order(user=user1, product=product1, quantity=1, status=False)
order2 = Order(user=user1, product=product2, quantity=2, status=True)
order3 = Order(user=user2, product=product3, quantity=3, status=False)
order4 = Order(user=user2, product=product1, quantity=1, status=True)

session.add_all([user1, user2, product1, product2, product3, order1, order2, order3, order4])
session.commit()

print("\nAll Users:")
for user in session.query(User).all():
    print(user.id, user.name, user.email)

print("\nAll Products:")
for product in session.query(Product).all():
    print(product.id, product.name, product.price)

print("\nAll Orders:")
for order in session.query(Order).all():
    print(order.id, order.user.name, order.product.name, order.quantity, "Shipped" if order.status else "Not Shipped")

product_to_update = session.query(Product).filter_by(name="Phone").first()
product_to_update.price = 750
session.commit()
print("\nUpdated Phone Price:", product_to_update.price)

user_to_delete = session.query(User).filter_by(id=2).first()
session.delete(user_to_delete)
session.commit()
print("\nDeleted User with ID 2")

print("\nOrders Not Shipped:")
for order in session.query(Order).filter_by(status=False).all():
    print(order.id, order.user.name, order.product.name, order.quantity)

print("\nTotal Orders per User:")
for user in session.query(User).all():
    count = session.query(Order).filter_by(user_id=user.id).count()
    print(user.name, "has", count, "orders")
