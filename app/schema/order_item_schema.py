from marshmallow import Schema, fields

class OrderItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    order_id = fields.Integer(required=True)
    animal_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    price = fields.Float(required=True)
    
order_item_schema = OrderItemSchema()
order_items_schema = OrderItemSchema(many=True)