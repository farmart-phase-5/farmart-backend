from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    role = fields.Str(validate=validate.OneOf(["client", "farmer", "admin"]))
    password = fields.Str(load_only=True, required=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
