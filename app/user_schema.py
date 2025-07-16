from marshmallow import Schema, fields, validate

class Register(Schema):
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, validate= validate.Length(min = 3))
    role = fields.Str(required=True, validate= validate.Oneof(['farmer', 'client']))

class Login(Schema):
    email = fields.Email(required= True)
    password = fields.Str(required=True)