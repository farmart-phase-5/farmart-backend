from farend.models import ma
from farend.models.order import Order
from marshmallow import fields, validates, ValidationError

class OrderSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Order
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    client_id = ma.auto_field(required=True)
    product_id = ma.auto_field(required=True)
    quantity = ma.auto_field(required=True)
    status = ma.auto_field()
    created_at = ma.auto_field()

    @validates('quantity')
    def validate_quantity(self, value):
        if value < 1:
            raise ValidationError("Quantity must be at least 1.")

    @validates('status')
    def validate_status(self, value):
        allowed_statuses = ['pending', 'confirmed', 'cancelled', 'completed']
        if value not in allowed_statuses:
            raise ValidationError(f"Invalid status '{value}'. Must be one of {allowed_statuses}.")
