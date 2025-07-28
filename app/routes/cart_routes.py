from flask import Blueprint, request, jsonify
from app import db
from app.models.cart import Cart
from app.models.cart_item import CartItem

cart_routes = Blueprint('cart_routes', __name__)


@cart_routes.route('/carts', methods=['POST'])
def create_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    status = data.get('status', 'pending')  

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    cart = Cart(user_id=user_id, status=status)
    db.session.add(cart)
    db.session.commit()
    return jsonify({
        'id': cart.id,
        'user_id': cart.user_id,
        'status': cart.status
    }), 201


@cart_routes.route('/carts', methods=['GET'])
def get_carts():
    status = request.args.get('status')
    query = Cart.query
    if status:
        query = query.filter_by(status=status)
    carts = query.all()
    return jsonify([{
        'id': cart.id,
        'user_id': cart.user_id,
        'status': cart.status
    } for cart in carts]), 200


@cart_routes.route('/carts/<int:id>', methods=['GET'])
def get_cart(id):
    cart = Cart.query.get(id)
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404

    return jsonify({
        'id': cart.id,
        'user_id': cart.user_id,
        'status': cart.status
    })


@cart_routes.route('/carts/<int:id>', methods=['PATCH', 'DELETE'])
def update_or_delete_cart(id):
    cart = Cart.query.get(id)
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404

    if request.method == 'PATCH':
        data = request.get_json()
        if 'status' in data:
            cart.status = data['status']
            db.session.commit()
        return jsonify({
            'id': cart.id,
            'user_id': cart.user_id,
            'status': cart.status
        }), 200

    elif request.method == 'DELETE':
        db.session.delete(cart)
        db.session.commit()
        return jsonify({'message': f'Cart {id} deleted successfully'}), 200


@cart_routes.route('/cart_items', methods=['POST'])
def add_item():
    data = request.get_json()
    cart_id = data.get('cart_id')
    animal_id = data.get('animal_id')
    quantity = data.get('quantity', 1)

    if not cart_id or not animal_id:
        return jsonify({'error': 'cart_id and animal_id are required'}), 400

    cart = Cart.query.get(cart_id)
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404

    item = CartItem(
        cart_id=cart_id,
        animal_id=animal_id,
        quantity=quantity,
        user_id=cart.user_id
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({
        'id': item.id,
        'cart_id': item.cart_id,
        'animal_id': item.animal_id,
        'quantity': item.quantity,
        'user_id': item.user_id
    }), 201


@cart_routes.route('/cart_items', methods=['GET'])
def get_items():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    items = CartItem.query.paginate(page=page, per_page=per_page, error_out=False)

    results = [{
        'id': item.id,
        'cart_id': item.cart_id,
        'animal_id': item.animal_id,
        'quantity': item.quantity
    } for item in items.items]

    return jsonify({
        'cart_items': results,
        'total': items.total,
        'pages': items.pages,
        'current_page': items.page
    })


@cart_routes.route('/cart_items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = CartItem.query.get(id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': f'Item {id} deleted successfully'})


@cart_routes.route('/cart_items/<int:id>', methods=['PATCH'])
def update_item(id):
    item = CartItem.query.get(id)
    if not item:
        return jsonify({'message': 'Cart item not found'}), 404

    data = request.get_json()
    quantity = data.get('quantity')
    animal_id = data.get('animal_id')

    if quantity is not None:
        item.quantity = quantity
    if animal_id is not None:
        item.animal_id = animal_id

    db.session.commit()
    return jsonify({
        'message': f'Cart item {id} updated successfully',
        'cart_id': item.cart_id,
        'animal_id': item.animal_id,
        'quantity': item.quantity
    })
