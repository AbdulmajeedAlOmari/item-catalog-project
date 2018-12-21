from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Drop all tables
Base.metadata.drop_all()

# Recreate tables
Base.metadata.create_all()

# Add users
# User1 = User(name="Abdulmajeed Alomari", email="abdulmajeedmmo@gmail.com")
# session.add(User1)
# session.commit()
#
# User2 = User(name="Nawaf Alquaid", email="nawaf.alquaid@gmail.com")
# session.add(User2)
# session.commit()


# Add categories
category1 = Category(name="Snowboarding")
session.add(category1)
session.commit()

category2 = Category(name="Soccer")
session.add(category2)
session.commit()

category3 = Category(name="Basketball")
session.add(category3)
session.commit()

category4 = Category(name="Football")
session.add(category4)
session.commit()

category5 = Category(name="Hockey")
session.add(category5)
session.commit()


# Add items
# [ User1 ]
item = Item(name="Stick", description="A stick that can be used.. etc..",
            category_id=category5.id)
session.add(item)
session.commit()

item = Item(name="Goggles", description="Goggles that can be used.. etc..",
            category_id=category1.id)
session.add(item)
session.commit()

item = Item(name="Snowboard", description="Snowbourd that can be used.. etc..",
            category_id=category1.id)
session.add(item)
session.commit()

# [ User2 ]
item = Item(name="Two Shinguards",
            description="Two Shinguards that can be used.. etc..",
            category_id=category2.id)
session.add(item)
session.commit()

item = Item(name="Shinguards",
            description="Shinguards that can be used.. etc..",
            category_id=category2.id)
session.add(item)
session.commit()

item = Item(name="Bat",
            description="A Bat that can be used.. etc..",
            category_id=category3.id)
session.add(item)
session.commit()

print("Database was seeded!")
