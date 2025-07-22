'''from flask import jsonify
from extensions import db
from farend.models.products import Product
from farend.schema.product_schema import validate_product_data, serialize_product, serialize_products

class ProductController:
    @staticmethod
    def create_product(data):
        validated_data, errors = validate_product_data(data)
        if errors:
            return jsonify({"error": errors}), 400

        new_product = Product(
            name=validated_data['name'],
            description=validated_data.get('description'),
            price=validated_data['price'],
            stock=validated_data['stock'],
            image_url=validated_data.get('image_url'),
            farmer_id=validated_data['farmer_id']
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product created successfully", "product": serialize_product(new_product)}), 201

    @staticmethod
    def get_products():
        products = Product.query.all()
        return jsonify({"products": serialize_products(products)}), 200

    @staticmethod
    def get_product(product_id):
        product = Product.query.get_or_404(product_id)
        return jsonify({"product": serialize_product(product)}), 200

    @staticmethod
    def update_product(product_id, data):
        product = Product.query.get_or_404(product_id)
        validated_data, errors = validate_product_data(data)
        if errors:
            return jsonify({"error": errors}), 400

        product.name = validated_data.get('name', product.name)
        product.description = validated_data.get('description', product.description)
        product.price = validated_data.get('price', product.price)
        product.stock = validated_data.get('stock', product.stock)
        product.image_url = validated_data.get('image_url', product.image_url)
        product.farmer_id = validated_data.get('farmer_id', product.farmer_id)
        db.session.commit()
        return jsonify({"message": "Product updated successfully", "product": serialize_product(product)}), 200

    @staticmethod
    def delete_product(product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200'''