from flask import Blueprint, request, jsonify, Response
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI
from validation import MedicamentSchema
from sqlalchemy import create_engine
from models import Medicament
from user import token_required_user

medicament = Blueprint('drug', __name__)
bcrypt = Bcrypt()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

session = Session()


@medicament.route('/drug/', methods=['POST'])
@token_required_user
def creatingDrug(current_user):
    if not current_user.role == 'worker' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for workers'})

    data = request.get_json(force=True)
    try:
        MedicamentSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    session.query(Medicament).filter_by(name=data['name']).first()
    session.query(Medicament).filter_by(price=data['price']).first()
    session.query(Medicament).filter_by(number=data['number']).first()
    users = Medicament(name=data['name'], price=data['price'], number=data['number'])
    session.add(users)
    session.commit()
    session.close()
    return Response(response="Drug successfully created")


@medicament.route('/drug/<id>', methods=['GET'])
def getDrugById(id):
    id = session.query(Medicament).filter_by(id=id).first()
    if not id:
        return Response(status=404, response="id doesn't exist")
    biblethump = {'id': id.id, 'name': id.name,  'price': id.price, 'number': id.number}
    return jsonify({'user': biblethump})


@medicament.route('/drugName/<string:name>', methods=['GET'])
def getDrugByName(name):
    id = session.query(Medicament).filter_by(name=name).first()
    if not id:
        return Response(status=404, response="id doesn't exist")
    biblethump = {'id': id.id, 'name': id.name,  'price': id.price, 'number': id.number}
    return jsonify({'user': biblethump})

@medicament.route('/drug', methods=['GET'])
def getDrugs():
    limbo = session.query(Medicament)
    quer = [MedicamentSchema().dump(i) for i in limbo]
    if not quer:
        return {"message": "No products available"}, 404
    res = {}
    for i in range(len(quer)):
        res[i + 1] = quer[i]
    return res


@medicament.route('/drug/<id>', methods=['PUT'])
@token_required_user
def updateDrug(current_user, id):
    if not current_user.role == 'worker' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for workers'})

    data = request.get_json(force=True)
    try:
        MedicamentSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    user_data = session.query(Medicament).filter_by(id=id).first()
    if not user_data:
        return Response(status=404, response="Id doesn't exist")
    if 'name' in data.keys():
        session.query(Medicament).filter_by(name=data['name']).first()

        user_data.name = data['name']

    if 'login' in data.keys():
        session.query(Medicament).filter_by(price=data['price']).first()
        user_data.login = data['price']


    if 'number' in data.keys():
        user_data.number = data['number']

    session.commit()
    session.close()
    return Response(response="Drug successfully updated")


@medicament.route('/drug/<id>', methods=['DELETE'])
@token_required_user
def deleteDrug(current_user, id):
    if not current_user.role == 'worker' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for workers'})
    id = session.query(Medicament).filter_by(id=id).first()
    if not id:
        return Response(status=404, response="ID doesn't exist")
    session.delete(id)
    session.commit()
    session.close()
    return Response(response="Drug successfully deleted")