from flask import Blueprint, request, jsonify, Response
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI
from validation import PurchaseSchema
from sqlalchemy import create_engine
from models import Purchase, User, Medicament
from user import token_required_user

purchase = Blueprint('purchase', __name__)
bcrypt = Bcrypt()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

session = Session()


@purchase.route('/purchase/', methods=['POST'])
@token_required_user
def creatingPurchase(current_user):
    if not current_user.role == 'user':
        return jsonify({'message': 'This is only for users'})
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
    return Response(response="Purchase successfully created")


@purchase.route('/purchase/<id>', methods=['GET'])
@token_required_user
def getPurchaseById(current_worker,  id):
    if not current_worker.role == 'worker' or current_worker.role == 'admin':
        return jsonify({'message': 'This is only for workers'})
    id = session.query(Purchase).filter_by(id=id).first()
    if not id:
        return Response(status=404, response="id doesn't exist")
    biblethump = {'id': id.id, 'user_id': id.user_id,  'product_id': id.product_id, 'number': id.number}
    return jsonify({'user': biblethump})


@purchase.route('/purchase', methods=['GET'])
@token_required_user
def getPurchases(current_user):
    if not current_user.role == 'worker' or current_user.role == 'admin' or current_user.role == 'user':
        return jsonify({'message': 'This is only for workers'})
    limbo = session.query(Purchase)
    quer = [PurchaseSchema().dump(i) for i in limbo]
    if not quer:
        return {"message": "No purchases available"}, 404
    res = {}
    for i in range(len(quer)):
        res[i + 1] = quer[i]
    return res



@purchase.route('/purchase/<id>', methods=['DELETE'])
@token_required_user
def deletePurchase(current_user, id):
    if not current_user.role == 'admin' or current_user.role == 'user':
        return jsonify({'message': 'This is only for workers'})
    id = session.query(Purchase).filter_by(id=id).first()
    if not id:
        return Response(status=404, response="ID doesn't exist")
    session.delete(id)
    session.commit()
    session.close()
    return Response(response="Purchase successfully deleted")