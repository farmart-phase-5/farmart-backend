from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3))
    description = fields.Str(required=True)
    price = fields.Float(required=True)
    quantity = fields.Int(required=True)
    category = fields.Str(required=True)
    image_url = fields.Url()
    farmer_id = fields.Int(required=True)
