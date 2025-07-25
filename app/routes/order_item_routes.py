from flask import Blueprint
from app.controllers.order_item_controller import (
    create_order_item,
    get_all_order_items,
    get_order_item,
    update_order_item,
    delete_order_item,
    get_order_items_by_order
)

order_item_routes = Blueprint('order_item_routes', __name__, url_prefix='/api/order-items')

# Create a new order item
order_item_routes.add_url_rule('', view_func=create_order_item, methods=['POST'])

# Get all order items
order_item_routes.add_url_rule('', view_func=get_all_order_items, methods=['GET'])

# Get a specific order item
order_item_routes.add_url_rule('/<int:order_item_id>', view_func=get_order_item, methods=['GET'])

# Update a specific order item
order_item_routes.add_url_rule('/<int:order_item_id>', view_func=update_order_item, methods=['PUT'])

# Delete a specific order item
order_item_routes.add_url_rule('/<int:order_item_id>', view_func=delete_order_item, methods=['DELETE'])

# Get all order items for a specific order
order_item_routes.add_url_rule('/order/<int:order_id>', view_func=get_order_items_by_order, methods=['GET'])