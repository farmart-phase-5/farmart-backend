from flask import request, jsonify
from farend.models.products import Product
from farend.schema.product_schema import product_schema, products_schema
from extensions import db

class ProductController:

    @staticmethod
    def get_all_products():
        products = Product.query.all()
        return products_schema.dump(products), 200

    @staticmethod
    def get_product(product_id):
        product = Product.query.get_or_404(product_id)
        return product_schema.dump(product), 200

    @staticmethod
    def create_product():
        data = request.get_json()
        product = product_schema.load(data)
        db.session.add(product)
        db.session.commit()
        return product_schema.dump(product), 201

    @staticmethod
    def update_product(product_id):
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        product = product_schema.load(data, instance=product, partial=True)
        db.session.commit()
        return product_schema.dump(product), 200

    @staticmethod
    def delete_product(product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted"}, 204
