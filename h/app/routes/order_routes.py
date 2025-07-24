from flask import Blueprint, request, jsonify
from app.models import Order, OrderItem
from app import db

order_routes = Blueprint('order_routes', __name__)


@order_routes.route('/', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders]), 200


@order_routes.route('/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    return jsonify(order.to_dict()), 200


@order_routes.route('/users/<int:user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([order.to_dict() for order in orders]), 200


@order_routes.route('/<int:order_id>/items', methods=['GET'])
def get_order_items(order_id):
    items = OrderItem.query.filter_by(order_id=order_id).all()
    return jsonify([item.to_dict() for item in items]), 200

@order_routes.route('/items', methods=['GET'])
def get_order_items_by_animal():
    animal_id = request.args.get('animal_id')
    if animal_id:
        items = OrderItem.query.filter_by(animal_id=animal_id).all()
        return jsonify([item.to_dict() for item in items]), 200
    return jsonify({"error": "animal_id parameter is required"}), 400


@order_routes.route('/', methods=['POST'])
def create_order():
    data = request.get_json(force=True)

    print('DEBUG Received JSON:', data) 

    user_id = data.get('user_id')
    farmer_id = data.get('farmer_id')
    animal_id = data.get('animal_id')
    quantity = data.get('quantity')
    status = data.get('status', 'pending')  

    if not all([user_id, farmer_id, animal_id, quantity]):
        return jsonify({'error': 'Missing required fields: user_id, farmer_id, animal_id, quantity'}), 400

    try:
        
        order = Order(user_id=user_id, farmer_id=farmer_id, status=status)
        db.session.add(order)
        db.session.commit()

       
        item = OrderItem(order_id=order.id, animal_id=animal_id, quantity=quantity)
        db.session.add(item)
        db.session.commit()

        return jsonify(order.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@order_routes.route('/<int:id>', methods=['PATCH'])
def update_order(id):
    order = Order.query.get_or_404(id)
    data = request.get_json()

   
    updatable_fields = ['status', 'farmer_notes']
    for field in updatable_fields:
        if field in data:
            setattr(order, field, data[field])

    db.session.commit()
    return jsonify(order.to_dict()), 200
