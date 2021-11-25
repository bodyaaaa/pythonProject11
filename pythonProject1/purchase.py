from flask import Blueprint, request, jsonify, Response
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI
from validation import PurchaseSchema
from sqlalchemy import create_engine
from models import Purchase, User, Medicament

purchase = Blueprint('purchase', __name__)
bcrypt = Bcrypt()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

session = Session()


@purchase.route('/orders/', methods=['POST'])
def creatingOrder():
    data = request.get_json(force=True)
    try:
        PurchaseSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    userid = session.query(User).filter_by(id=data['user_id']).first()
    if not userid:
        return Response(status=404, response="User_id doesn't exist")
    productid = session.query(Medicament).filter_by(id=data['product_id']).first()
    if not productid:
        return Response(status=404, response="product id doesn't exist")
    session.query(Purchase).filter_by(number=data['number']).first()
    users = Purchase(user_id=data['user_id'], product_id=data['product_id'], number=data['number'])
    session.add(users)
    session.commit()
    session.close()
    return Response(response="Order successfully created")


@purchase.route('/orders/<id>', methods=['GET'])
def getOrderById(id):
    id = session.query(Purchase).filter_by(id=id).first()
    if not id:
        return Response(status=404, response="id doesn't exist")
    biblethump = {'id': id.id, 'user_id': id.user_id,  'product_id': id.product_id, 'number': id.number}
    return jsonify({'user': biblethump})


@purchase.route('/orders', methods=['GET'])
def getOrders():
    limbo = session.query(Purchase)
    quer = [PurchaseSchema().dump(i) for i in limbo]
    if not quer:
        return {"message": "No orders available"}, 404
    res = {}
    for i in range(len(quer)):
        res[i + 1] = quer[i]
    return res


@purchase.route('/orders/<id>', methods=['DELETE'])
def deleteOrder(id):
    id = session.query(Purchase).filter_by(id=id).first()
    if not id:
        return Response(status=404, response="ID doesn't exist")
    session.delete(id)
    session.commit()
    session.close()
    return Response(response="Order successfully deleted")