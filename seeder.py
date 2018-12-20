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
User1 = User(name="Abdulmajeed Alomari", email="abdulmajeedmmo@gmail.com")
session.add(User1)
session.commit()

User2 = User(name="Nawaf Alquaid", email="nawaf.alquaid@gmail.com")
session.add(User2)
session.commit()


# Add categories
category1 = Category(
            name="Snowboarding",
            pic="""
            https://farm4.staticflickr.com/3710/11358281146_34af67826f.jpg
            """
        )
session.add(category1)
session.commit()

category2 = Category(
            name="Soccer",
            pic="""
            https://9b16f79ca967fd0708d1-2713572fef44aa49ec323e813b06d2d9.ssl.cf2.rackcdn.com/1140x_a10-7_cTC/LIFE-EDU-SOCCER-SUED-MCT-1542165981.jpg
            """
            )
session.add(category2)
session.commit()

category3 = Category(
            name="Basketball",
            pic="""
            https://pixabay.com/get/e135b00828fc1c22d2524518b7444795ea76e5d004b0144590f3c37ba0eeb0_340.jpg
            """
            )
session.add(category3)
session.commit()

category4 = Category(
            name="Football",
            pic="""
            https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTq1xrYvsjOgXSo2BhqSctfl0YCqmwqR15GJWQlmeDL9O6bOOEb
            """
            )
session.add(category4)
session.commit()

category5 = Category(
            name="Hockey",
            pic="""
            https://www.macleans.ca/wp-content/uploads/2017/06/JUNE30_BRUNT_HOCKEY_POST01.jpg
            """)
session.add(category5)
session.commit()


# Add items
# [ User1 ]
item = Item(name="Stick", description="A stick that can be used.. etc..",
            category_id=category5.id, user_id=User1.id)
session.add(item)
session.commit()

item = Item(name="Goggles", description="Goggles that can be used.. etc..",
            category_id=category1.id, user_id=User1.id)
session.add(item)
session.commit()

item = Item(name="Snowboard", description="Snowbourd that can be used.. etc..",
            category_id=category1.id, user_id=User1.id)
session.add(item)
session.commit()

# [ User2 ]
item = Item(name="Two Shinguards",
            description="Two Shinguards that can be used.. etc..",
            category_id=category2.id, user_id=User2.id)
session.add(item)
session.commit()

item = Item(name="Shinguards",
            description="Shinguards that can be used.. etc..",
            category_id=category2.id, user_id=User2.id)
session.add(item)
session.commit()

item = Item(name="Bat",
            description="A Bat that can be used.. etc..",
            category_id=category3.id, user_id=User2.id)
session.add(item)
session.commit()

print("Database was seeded!")
