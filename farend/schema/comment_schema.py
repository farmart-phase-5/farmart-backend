from marshmallow import Schema, fields

class CommentSchema(Schema):
    id = fields.Int()
    content = fields.Str(required=True)
    timestamp = fields.DateTime()
    user = fields.Nested(lambda: UserSchema(only=("id", "username")))

from .user_schema import UserSchema
commentschema = CommentSchema()
comments_schema = CommentSchema(many=True)
