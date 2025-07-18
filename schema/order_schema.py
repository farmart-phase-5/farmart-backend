from marshmallow import Schema, fields, validate

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    total_price = fields.Float(dump_only=True)
    status = fields.Str(
        required=True,
        validate=validate.OneOf(["pending", "approved", "rejected", "delivered"])
    )
    created_at = fields.DateTime(dump_only=True)
