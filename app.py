from flask import Flask, request, make_response
from flask import render_template
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/data.db'
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/menu', methods=['GET'])
def testmenu():
    return render_template('menu.html')


if __name__ == '__main__':
    app.run(debug=True)
