'''from farend.models.products import Product

def validate_product_data(data):
    errors = []
    validated_data = {}

    if 'name' not in data or not data['name']:
        errors.append("Name is required.")
    else:
        validated_data['name'] = data['name']

    if 'description' in data:
        validated_data['description'] = data['description']

    if 'price' not in data or not isinstance(data['price'], (int, float)) or data['price'] < 0:
        errors.append("Price is required and must be a non-negative number.")
    else:
        validated_data['price'] = data['price']

    if 'stock' not in data or not isinstance(data['stock'], int) or data['stock'] < 0:
        errors.append("Stock is required and must be a non-negative integer.")
    else:
        validated_data['stock'] = data['stock']

    if 'image_url' in data:
        validated_data['image_url'] = data['image_url']

    if 'farmer_id' not in data or not isinstance(data['farmer_id'], int):
        errors.append("Farmer ID is required and must be an integer.")
    else:
        validated_data['farmer_id'] = data['farmer_id']

    return validated_data, errors

def serialize_product(product):
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': float(product.price),
        'stock': product.stock,
        'image_url': product.image_url,
        'created_at': product.created_at.isoformat() if product.created_at else None,
        'updated_at': product.updated_at.isoformat() if product.updated_at else None,
        'farmer_id': product.farmer_id
    }

def serialize_products(products):
    return [serialize_product(product) for product in products]'''