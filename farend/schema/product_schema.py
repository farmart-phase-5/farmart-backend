from marshmallow import Schema, fields

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    stock = fields.Int()
    description = fields.Str()

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
