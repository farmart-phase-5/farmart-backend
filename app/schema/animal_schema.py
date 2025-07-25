from marshmallow import Schema, fields

class AnimalSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    species = fields.String(required=True)
    breed = fields.String()
    age = fields.Integer()
    farmer_id = fields.Integer(required=True)
    
animal_schema = AnimalSchema()
animals_schema = AnimalSchema(many=True)