from marshmallow import Schema, fields

class OrderSchema(Schema):
    id = fields.Integer(dump_only=True)
    animal_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    total_price = fields.Float(required=True)
    status = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)