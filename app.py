from typing import Any, Union

from flask import Flask, request, session
from flask import render_template
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "sEcReTkEy"
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/data.db'

db = SQLAlchemy(app)

cart = []


class MenuItem(db.Model):
    __tablename__ = 'MenuItem'
    MenuItemId = db.Column(db.Integer, primary_key=True)
    ItemType = db.Column(db.Text)
    ItemName = db.Column(db.Text)
    BaseCost = db.Column(db.Numeric)
    AllowExtras = db.Column(db.Text)

    def __repr__(self):
        return '<MenuItem %r>' % self.ItemName


class ExtraItems(db.Model):
    __tablename__ = 'ExtraItems'
    ExtraId = db.Column(db.Integer, primary_key=True)
    ExtraName = db.Column(db.Text)
    ExtraCost = db.Column(db.Numeric)

    def __repr__(self):
        return '<ExtraItems %r>' % self.ExtraId


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/menu', methods=['GET'])
def testMenu():
    test1 = []
    test2 = ['None']
    test = MenuItem.query.all()
    for item in test:
        test1.append(item.ItemName)
    Extratest = ExtraItems.query.all()
    for extra in Extratest:
        test2.append(extra.ExtraName)
    return render_template('menu.html', test1=test1, test2=test2)


@app.route('/reviewOrder', methods=['POST'])
def testsubmit():
    total = 0
    currentOrder = [request.form.get("main_item"), request.form.get("extra_item")]
    cart.extend(currentOrder)
    for y in cart:
        z = MenuItem.query.filter_by(ItemName=y).first()
        if z is not None:
            cost = float(z.BaseCost)
            total = total + cost
        q = ExtraItems.query.filter_by(ExtraName=y).first()
        if q is not None:
            extra_cost = float(q.ExtraCost)
            total = total + extra_cost
    session['total_form'] = "${:,.2f}".format(total)
    return render_template('checkout.html', cart=cart, total=session['total_form'])


@app.route('/userInfo', methods=['POST'])
def show_user_info():
    return render_template('details.html', total=session['total_form'])


@app.route('/finalized', methods=['POST'])
def store_data():

    return render_template('finalize.html')


if __name__ == '__main__':
    app.run(debug=True)
