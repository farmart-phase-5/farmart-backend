from extensions import db
from farend.models.order import Order
from farend.schema.order_schema import OrderSchema

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

class OrderController:

    def create_order(self, data):
        new_order = order_schema.load(data)
        order = Order(**new_order)
        db.session.add(order)
        db.session.commit()
        return order_schema.dump(order)

    def get_all_orders(self):
        orders = Order.query.all()
        return orders_schema.dump(orders)

    def update_order(self, order_id, data):
        order = Order.query.get(order_id)
        if not order:
            raise Exception("Order not found.")
        
        for key, value in data.items():
            setattr(order, key, value)

        db.session.commit()
        return order_schema.dump(order)

    def delete_order(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            raise Exception("Order not found.")

        db.session.delete(order)
        db.session.commit()
        return {"message": f"Order #{order_id} deleted successfully."}
