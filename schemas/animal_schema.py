from marshmallow import Schema,fields

class AnimalSchema(Schema):
    id=fields.Int()
    name=fields.Str()
    breed=fields.Str()
    price=fields.Float()

animalschema=AnimalSchema()