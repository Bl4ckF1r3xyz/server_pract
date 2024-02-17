from decimal import Decimal
from datetime import datetime
from pony.converting import str2datetime
from pony.orm import *
db = Database()
class Customer(db.Entity):
    email = Required(str, unique=True)
    password = Required(str)
    name = Required(str)
    country = Required(str)
    address = Required(str)
    cart_items = Set('CartItem')
    orders = Set('Order')


class Product(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    categories = Set('Category')
    description = Optional(str)
    picture = Optional(buffer)
    price = Required(Decimal)
    quantity = Required(int)
    cart_items = Set('CartItem')
    order_items = Set('OrderItem')


class CartItem(db.Entity):
    quantity = Required(int)
    customer = Required(Customer)
    product = Required(Product)


class OrderItem(db.Entity):
    quantity = Required(int)
    price = Required(Decimal)
    order = Required('Order', reverse='order_items')
    product = Required(Product)
    PrimaryKey(order, product)


class Order(db.Entity):
    id = PrimaryKey(int, auto=True)
    state = Required(str)
    date_created = Required(datetime)
    date_shipped = Optional(datetime)
    date_delivered = Optional(datetime)
    total_price = Required(Decimal)
    customer = Required(Customer)
    order_items = Set(OrderItem)


class Category(db.Entity):
    name = Required(str, unique=True)
    products = Set(Product)


set_sql_debug(True)
db.bind('sqlite', 'estore.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

def populate_database():
    with db_session:
        customer1 = Customer(email='john@example.com', password='password123',
                             name='John Doe', country='USA', address='123 Main St')
        customer2 = Customer(email='jane@example.com', password='securepass',
                             name='Jane Smith', country='Canada', address='456 Maple Ave')

        product1 = Product(name='Laptop', description='Powerful laptop', price=999.99, quantity=10)
        product2 = Product(name='Tablet', description='High-quality tablet', price=499.99, quantity=5)

        category1 = Category(name='Computers', products=[product1])
        category2 = Category(name='Tablets', products=[product2])

        order1 = Order(state='SHIPPED', date_created=datetime.now(), total_price=999.99, customer=customer1)
        order2 = Order(state='DELIVERED', date_created=datetime.now(), total_price=499.99, customer=customer2)

        order_item1 = OrderItem(quantity=1, price=999.99, order=order1, product=product1)
        order_item2 = OrderItem(quantity=2, price=499.99, order=order2, product=product2)

        commit()

populate_database()