#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    response = make_response([bakery.to_dict() for bakery in Bakery.query.all()], 200)
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    single_bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_dict = single_bakery.to_dict()
    response = (bakery_dict, 200)

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    response = make_response([goods.to_dict() for goods in BakedGood.query.order_by(desc(BakedGood.price)).all()], 200)

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(desc(BakedGood.price)).limit(1).first()
    response = (most_expensive.to_dict(), 200)

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
