from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from farend.controllers.product_controllers import ProductController

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    return ProductController.get_all()

@product_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    farmer_id = get_jwt_identity()
    return ProductController.create(data, farmer_id)

@product_bp.route('/products/<int:product_id>', methods=['PATCH'])
@jwt_required()
def update_product(product_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    return ProductController.update(product_id, data, user_id)

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    user_id = get_jwt_identity()
    return ProductController.delete(product_id, user_id)
