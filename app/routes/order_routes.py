from flask import Blueprint, request, jsonify
from app import db
from app.models.order_model import Order
from app.models.order_item_model import OrderItem

order_routes = Blueprint('order_routes', __name__)

# --------------------------
# GET all orders with optional status filtering
@order_routes.route('/', methods=['GET'])
def get_orders():
    status = request.args.get('status')
    query = Order.query
    if status:
        query = query.filter_by(status=status)
    orders = query.all()
    return jsonify([order.to_dict() for order in orders]), 200

# --------------------------
# POST a new order
@order_routes.route('/', methods=['POST'])
def create_order():
    data = request.get_json()

    user_id = data.get('user_id')
    farmer_id = data.get('farmer_id')
    animal_id = data.get('animal_id')
    quantity = data.get('quantity')
    status = data.get('status', 'pending')
    farmer_notes = data.get('farmer_notes')

    # Validate required fields
    if not all([user_id, farmer_id, animal_id, quantity]):
        return jsonify({'error': 'Missing required fields: user_id, farmer_id, animal_id, quantity'}), 400

    try:
        # Create order
        new_order = Order(
            user_id=user_id,
            farmer_id=farmer_id,
            status=status,
            farmer_notes=farmer_notes
        )
        db.session.add(new_order)
        db.session.commit()

        # Create order item
        new_item = OrderItem(
            order_id=new_order.id,
            animal_id=animal_id,
            quantity=quantity
        )
        db.session.add(new_item)
        db.session.commit()

        return jsonify(new_order.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# --------------------------
# GET a single order by ID
@order_routes.route('/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    return jsonify(order.to_dict()), 200

# --------------------------
# GET all orders for a specific user
@order_routes.route('/users/<int:user_id>/orders', methods=['GET'])
def get_orders_by_user(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([order.to_dict() for order in orders]), 200

# --------------------------
# GET all items for a specific order
@order_routes.route('/<int:order_id>/items', methods=['GET'])
def get_order_items(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify([item.to_dict() for item in order.order_items]), 200

# --------------------------
# GET all order items by animal_id
@order_routes.route('/order_items', methods=['GET'])
def get_order_items_by_animal():
    animal_id = request.args.get('animal_id', type=int)
    if animal_id is None:
        return jsonify({'error': 'animal_id query parameter is required'}), 400

    items = OrderItem.query.filter_by(animal_id=animal_id).all()
    return jsonify([item.to_dict() for item in items]), 200
