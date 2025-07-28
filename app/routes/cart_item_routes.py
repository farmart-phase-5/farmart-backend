from flask import Blueprint, request, jsonify
from app import db
from app.models.cart_item import CartItem
from app.models.cart import Cart

cart_item_routes = Blueprint('cart_item_routes', __name__)



@cart_item_routes.route('/cart_items', methods=['GET'])
def get_cart_items():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    cart_items = CartItem.query.paginate(page=page, per_page=per_page, error_out=False)

    result = [{
        'id': item.id,
        'cart_id': item.cart_id,
        'animal_id': item.animal_id,
        'quantity': item.quantity
    } for item in cart_items.items]

    return jsonify({
        'cart_items': result,
        'total': cart_items.total,
        'page': cart_items.page,
        'per_page': cart_items.per_page
    }), 200



@cart_item_routes.route('/cart_items', methods=['POST'])
def create_cart_item():
    data = request.get_json()
    cart_id = data.get('cart_id')
    animal_id = data.get('animal_id')
    quantity = data.get('quantity', 1)

    if not cart_id or not animal_id:
        return jsonify({'message': 'cart_id and animal_id are required'}), 400

    new_item = CartItem(cart_id=cart_id, animal_id=animal_id, quantity=quantity)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({
        'message': 'Cart item added successfully',
        'cart_item': {
            'id': new_item.id,
            'cart_id': new_item.cart_id,
            'animal_id': new_item.animal_id,
            'quantity': new_item.quantity
        }
    }), 201



@cart_item_routes.route('/cart_items/<int:item_id>', methods=['PATCH'])
def update_cart_item_quantity(item_id):
    data = request.get_json()
    item = CartItem.query.get(item_id)

    if not item:
        return jsonify({'message': 'Cart item not found'}), 404

    new_quantity = data.get('quantity')
    if new_quantity is not None:
        item.quantity = new_quantity
        db.session.commit()

    return jsonify({'message': 'Quantity updated successfully'}), 200



@cart_item_routes.route('/carts/<int:cart_id>/items', methods=['DELETE'])
def clear_cart_items(cart_id):
    cart = Cart.query.get(cart_id)

    if not cart:
        return jsonify({'message': 'Cart not found'}), 404

    CartItem.query.filter_by(cart_id=cart_id).delete()
    db.session.commit()

    return jsonify({'message': 'Cart cleared successfully'}), 200



@cart_item_routes.route('/carts', methods=['GET'])
def get_carts_by_status():
    status = request.args.get('status')
    if not status:
        return jsonify({'message': 'Status query parameter is required'}), 400

    carts = Cart.query.filter_by(status=status).all()
    result = [cart.to_dict() for cart in carts]

    return jsonify({'carts': result}), 200
