from marshmallow import Schema, fields
from marshmallow.validate import Length


class UserSchema(Schema):
    name = fields.String(validate=Length(min=4))
    login = fields.Email()
    password = fields.String(validate=Length(min=8))
    role = fields.String()


class MedicamentSchema(Schema):
    name = fields.String(required=True)
    price = fields.Float(required=True)
    number = fields.Integer(required=True)


class PurchaseSchema(Schema):
    user_id = fields.Integer(required=True)
    product_id = fields.Integer(required=True)
    number = fields.Integer(required=True)
