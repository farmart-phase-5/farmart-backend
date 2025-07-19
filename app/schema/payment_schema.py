from app import ma
from app.models.payment import Payment
from app.schema.user_schema import UserSchema
from app.schema.order_schema import OrderSchema


class PaymentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Payment
        load_instance = True

    id = ma.auto_field()
    amount = ma.auto_field()
    status = ma.auto_field()
    created_at = ma.auto_field()

    user = ma.Nested(UserSchema(only=("id", "username", "email")))
    order = ma.Nested(OrderSchema(only=("id", "quantity", "status")))
