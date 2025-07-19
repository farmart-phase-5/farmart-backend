from flask import request, jsonify
from app.models.products import Product
from app import db
from app.schema.product_schema import ProductSchema

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

def get_products():
    products = Product.query.all()
    return jsonify(products_schema.dump(products)), 200

def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product_schema.dump(product)), 200

def create_product():
    data = request.get_json()
    errors = product_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        quantity_available=data['quantity_available'],
        farmer_id=data['farmer_id']
    )

    db.session.add(new_product)
    db.session.commit()
    return jsonify(product_schema.dump(new_product)), 201

def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()

    errors = product_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.quantity_available = data.get('quantity_available', product.quantity_available)
    product.farmer_id = data.get('farmer_id', product.farmer_id)

    db.session.commit()
    return jsonify(product_schema.dump(product)), 200

def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 204
