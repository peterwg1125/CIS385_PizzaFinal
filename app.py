from typing import Any, Union

from flask import Flask, request, session
from flask import render_template
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import random


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


class Customer(db.Model):
    __tablename__ = 'Customer'
    CustomerId = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.Text)
    LastName = db.Column(db.Text)
    PhoneNumber = db.Column(db.Text)
    Street = db.Column(db.Text)
    City = db.Column(db.Text)

    def __repr__(self):
        return '<Customer %r>' % self.CustomerId


class Order(db.Model):
    __tablename__ = 'Order'
    OrderId = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Text)
    Time = db.Column(db.Text)
    CustomerId = db.Column(db.Integer)
    CustomerName = db.Column(db.Text)
    CustomerPhone = db.Column(db.Text)

    def __repr__(self):
        return '<Order %r>' % self.OrderId


class OrderItem(db.Model):
    __tablename__ = 'OrderItem'
    OrderItemId = db.Column(db.Integer, primary_key=True)
    OrderId = db.Column(db.Integer)
    MenuItemId = db.Column(db.Integer)
    ExtraId = db.Column(db.Integer)

    def __repr__(self):
        return '<OrderItem %r>' % self.OrderItemId


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


@app.route('/userInfo', methods=['GET'])
def show_user_info():
    return render_template('details.html', total=session['total_form'])


@app.route('/finalized', methods=['POST'])
def store_data():
    ID = random.randint(10, 200)
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    phone_num = request.form.get("phoneNum")
    street = request.form.get("street")
    city = request.form.get("city")
    # add to Customer Table
    new_customer = Customer(CustomerId=ID, FirstName=fname, LastName=lname, PhoneNumber=phone_num,
                            Street=street, City=city)
    db.session.add(new_customer)
    db.session.commit()
    # add to Order Table
    order_id = random.randint(10, 200)
    new_order = Order(OrderId=order_id, Date="2021-03-20", Time="15:00", CustomerId=ID,
                      CustomerName=(fname+" "+lname), CustomerPhone=phone_num)
    db.session.add(new_order)
    db.session.commit()
    # add to OrderItem Table
    extra_id = None
    menu_id = None
    for item in cart:
        t = MenuItem.query.filter_by(ItemName=item).first()
        if t is not None:
            menu_id = t.MenuItemId
        r = ExtraItems.query.filter_by(ExtraName=item).first()
        if r is not None:
            extra_id = r.ExtraId
        if menu_id is not None and extra_id is not None:
            new_orderItem = OrderItem(OrderItemId=random.randint(10, 200), OrderId=order_id, MenuItemId=menu_id, ExtraId=extra_id)
            db.session.add(new_orderItem)
            db.session.commit()
            extra_id = None
            menu_id = None
    return render_template('finalize.html')


if __name__ == '__main__':
    app.run(debug=True)
