from flask import Blueprint, request, jsonify
from models.cart import Cart, CartItem
from models.animals import Animals
from extension import db

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/', methods=['GET'])
def view_cart():
    user_id = request.args.get('user_id')
    cart = Cart.query.filter_by(user_id=user_id, status='open').first()
    if not cart:
        return jsonify({"cart": [], "message": "Empty cart"})

    items = [{
        "id": item.id,
        "animal_id": item.animal_id,
        "price": item.price,
        "quantity": item.quantity
    } for item in cart.items]

    return jsonify({"cart": items})

@cart_bp.route('/', methods=['POST'])
def add_to_cart():
    data = request.json
    user_id = data.get('user_id')
    animal_id = data.get('animal_id')

    animal = Animals.query.get(animal_id)
    if not animal or not animal.available:
        return jsonify({"error": "Animal not available"}), 400

    cart = Cart.query.filter_by(user_id=user_id, status='open').first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()

    item = CartItem(cart_id=cart.id, animal_id=animal.id, price=animal.price)
    db.session.add(item)
    db.session.commit()

    return jsonify({"message": "Added to cart", "item_id": item.id})

@cart_bp.route('/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Removed from cart"})
