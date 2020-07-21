# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 02:32:34 2020

@author: gcapote
"""
import psycopg2
from sqlalchemy import MetaData
metadata = MetaData()


from datetime import datetime
from sqlalchemy import Table, Column, Integer, Numeric, String, ForeignKey, DateTime
from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:')

cookies = Table('cookies', metadata,
    Column('cookie_id', Integer(), primary_key=True),
    Column('cookie_name', String(50), index=True),
    Column('cookie_recipe_url', String(255)),
    Column('cookie_sku', String(55)),
    Column('quantity', Integer()),
    Column('unit_cost', Numeric(12, 2))
)


users = Table('users', metadata,
    Column('user_id', Integer(), primary_key=True),
    Column('username', String(15), nullable=False, unique=True),
    Column('email_address', String(255), nullable=False),
    Column('phone', String(20), nullable=False),
    Column('password', String(25), nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

orders = Table('orders', metadata,
    Column('order_id', Integer(), primary_key=True),
    Column('user_id', ForeignKey('users.user_id')),
)

line_items = Table('line_items', metadata,
    Column('line_items_id', Integer(), primary_key=True),
    Column('order_id', ForeignKey('orders.order_id')),
    Column('cookie_id', ForeignKey('cookies.cookie_id')),
    Column('quantity', Integer()),
    Column('extended_cost', Numeric(12, 2))
)

metadata.create_all(engine)

connection = engine.connect()

ins = cookies.insert().values(
    cookie_name="chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
    cookie_sku="CC01",
    quantity="12",
    unit_cost="0.50"
)
print(str(ins))

ins.compile().params


result = connection.execute(ins)

result.inserted_primary_key



from sqlalchemy import insert
ins = insert(cookies).values(
    cookie_name="chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
    cookie_sku="CC01",
    quantity="12",
    unit_cost="0.50"
)
str(ins)


ins = cookies.insert()
result = connection.execute(ins, cookie_name='dark chocolate chip',
                            cookie_recipe_url='http://some.aweso.me/cookie/recipe_dark.html',
                            cookie_sku='CC02',
                            quantity='1',
                            unit_cost='0.75')


result.inserted_primary_key

# _______________________________

inventory_list = [
    {
        'cookie_name': 'peanut butter',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/peanut.html',
        'cookie_sku': 'PB01',
        'quantity': '24',
        'unit_cost': '0.25'
    },
    {
        'cookie_name': 'oatmeal raisin',
        'cookie_recipe_url': 'http://some.okay.me/cookie/raisin.html',
        'cookie_sku': 'EWW01',
        'quantity': '100',
        'unit_cost': '1.00'
    }
]

result = connection.execute(ins, inventory_list)

# ___________________________________


from sqlalchemy.sql import select

s = select([cookies])

str(s)

## ___________________________

rp = connection.execute(s)



results = rp.fetchall()

first_row = results[0]


first_row[3]

first_row.cookie_name

first_row[cookies.c.cookie_name]

# ____________________

s = cookies.select()

rp = connection.execute(s)


for record in rp:
    print(record.cookie_name)
# ________________________________
    
s = select([cookies.c.cookie_name, cookies.c.quantity])
rp = connection.execute(s)
print(rp.keys())
results = rp.fetchall()

results
# _________________________________________

s = select([cookies.c.cookie_name, cookies.c.quantity])
s = s.order_by(cookies.c.quantity, cookies.c.cookie_name)
rp = connection.execute(s)
for cookie in rp:
    print('{} - {}'.format(cookie.quantity, cookie.cookie_name))

## ________________________________________
    
from sqlalchemy import desc
s = select([cookies.c.cookie_name, cookies.c.quantity])
s = s.order_by(desc(cookies.c.quantity))
rp = connection.execute(s)
for cookie in rp:
    print('{} - {}'.format(cookie.quantity, cookie.cookie_name))