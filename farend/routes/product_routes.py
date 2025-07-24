'''from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from farend.controllers.product_controllers import ProductController

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    return ProductController.create_product(data)

@product_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    return ProductController.get_products()

@product_bp.route('/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    return ProductController.get_product(product_id)

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    data = request.get_json()
    return ProductController.update_product(product_id, data)

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    return ProductController.delete_product(product_id)'''