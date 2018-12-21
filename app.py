from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
# from flask import session as login_session
# import random
# import string
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.client import FlowExchangeError
# import httplib2
# import json
# from flask import make_response
# import requests

app = Flask(__name__)

# CLIENT_ID = json.loads(
#                 open('client_secrets.json', 'r').read()
#             )['web']['client_id']
# APPLICATION_NAME = "Item Catalog"


# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Retrieve all categories to render them in the templates
categories = session.query(Category).all()


# Landing route
@app.route('/')
def showHome():
    return render_template('landing.html')


# Authentication route [ Form / Authenticate ]
@app.route('/login')
def showLogin():
    return render_template('login.html')


# Index route [ Read ]
@app.route('/catalog')
def showCatalog():
    items = session.query(Item).order_by(
                                    Item.created_date.desc()
                                ).limit(10).all()

    return render_template(
                'index.html',
                recentlyAddedItems=items
            )


@app.route('/catalog/<string:category_name>')
def showCategory(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()

    return render_template(
            'categories/show.html',
            items=items,
            category_name=category_name,
        )


# New Item route [ Form / Create ]
@app.route('/catalog/new', methods=["GET", "POST"])
def newItem():
    if request.method == "POST":
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=request.form['category'],
        )
        session.add(newItem)
        session.commit()

        flash("Item was successfully added.")
        return redirect(url_for("showCatalog"))

    return render_template('items/new.html')


# Show Item route [ Read ]
@app.route('/catalog/<string:category>/<int:item_id>')
def showItem(category, item_id):
    item = session.query(Item).filter_by(id=item_id).one()

    if item:
        return render_template('items/show.html', item=item)
    else:
        return redirect(url_for("showCatalog"))


# Edit Item route [ Form / Update ]
@app.route('/catalog/<string:category>/<int:item_id>/edit', methods=[
    "GET", "POST"])
def editItem(category, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == "POST":
        if (request.form['name']
                and request.form['description']
                and request.form['category']):
            item.name = request.form['name']
            item.description = request.form['description']
            item.category_id = request.form['category']
            flash("Item successfully edited.")
            return redirect(url_for(
                "showItem",
                category=item.category.name,
                item_id=item.id)
            )

    return render_template('items/edit.html', item=item)


# Delete Item route [ Confirmation / Delete ]
@app.route('/catalog/<string:category>/<int:item_id>/delete', methods=[
    "GET", "POST"])
def deleteItem(category, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == "POST":
        session.delete(item)
        session.commit()
        flash("Successfully deleted item.")
        return redirect(url_for("showCatalog"))

    return render_template('items/delete.html', item=item)


# Pass categories to all templates (Global Variable)
@app.context_processor
def context_processor():
    return dict(categories=categories)


if __name__ == '__main__':
    app.secret_key = '$up3r_$eCr3T_K3Y'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
