from marshmallow import Schema, fields

class CommentSchema(Schema):
    id = fields.Int()
    content = fields.Str(required=True)
    timestamp = fields.DateTime()
    user = fields.Nested(lambda: UserSchema(only=("id", "username")))

from schema.user_schema import UserSchema
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
