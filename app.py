from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from database_setup import Base, Category, Item, User
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
APPLICATION_NAME = "Item Catalog"


# Connect to Database and create database session
# engine = create_engine('sqlite:///catalog.db')
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# session = DBSession()


@app.route('/')
def showHome():
    return render_template('landing.html')


@app.route('/login')
def showLogin():
    return render_template('login.html')


@app.route('/catalog')
def showCatalogs():
    return render_template('index.html')


@app.route('/catalog/<string:category>')
def showCategory(category):
    return render_template('categories/show.html')


@app.route('/catalog/new')
def newItem():
    return render_template('items/new.html')


@app.route('/catalog/<string:category>/<int:item_id>/edit')
def editItem(category, item_id):
    return render_template('items/edit.html')


@app.route('/catalog/<string:category>/<int:item_id>/delete')
def deleteItem(category, item_id):
    return render_template('items/delete.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
