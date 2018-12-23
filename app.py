from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# Load from client_secret.json
CLIENT_ID = json.loads(
                open('client_secret.json', 'r').read()
            )['web']['client_id']

# Define app
app = Flask(__name__)

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


# START Authentication routes
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.
                    digits) for x in xrange(32))

    login_session['state'] = state

    # Pass the state of the user
    return render_template("login.html", STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
                        json.dumps(
                            'Failed to upgrade the authorization code.',
                            401,
                        )
                    )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)

    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
                json.dumps('Current user is already connected.'), 200
            )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo?alt=json"
    userinfo_url += "&access_token=%s" % credentials.access_token
    answer = requests.get(userinfo_url)

    data = answer.json()

    print("------------- All data -------------")
    for key in data:
        print("[ {} ] --> {}".format(key, data[key]))
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '" style = "width: 300px; height: 300px;border-radius: 150px;" '
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    flash("you are now logged in as %s" % login_session['username'])
    return output


@app.route('/gdisconnect', methods=['POST'])
def gdisconnect():
    if not isLoggedIn():
        return redirect(url_for('showLogin'))

    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
                        json.dumps('Current user not connected.'),
                        401
                    )
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke'
    url += '?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
                        json.dumps(
                            'Failed to revoke token for given user.',
                            400
                        )
                    )
        response.headers['Content-Type'] = 'application/json'
        return response
# END authentication routes


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


# Helper methods
def isLoggedIn():
    return 'username' in login_session


# Pass global variables/methods to all templates
@app.context_processor
def context_processor():
    return dict(categories=categories, isLoggedIn=isLoggedIn)


if __name__ == '__main__':
    app.secret_key = '$up3r_$eCr3T_K3Y'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
