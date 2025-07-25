from marshmallow import Schema, fields

class FarmerSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    
farmer_schema = FarmerSchema()
farmers_schema = FarmerSchema(many=True)