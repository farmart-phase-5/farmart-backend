from flask import jsonify, request
from ..models.clients import Client
from ..extensions import db

def create_client(data):
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    role = data.get('role', 'client')

    if not username or not email:
        return jsonify({'error': 'Username and email are required'}), 400

    if Client.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409

    if Client.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 409

    new_client = Client(username=username, email=email, phone=phone, role=role)
    db.session.add(new_client)
    db.session.commit()

    return jsonify({
        'id': new_client.id,
        'username': new_client.username,
        'email': new_client.email,
        'phone': new_client.phone,
        'role': new_client.role
    }), 201


def get_all_clients():
    clients = Client.query.all()
    return jsonify([{
        'id': client.id,
        'username': client.username,
        'email': client.email,
        'phone': client.phone,
        'role': client.role
    } for client in clients]), 200


def get_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    return jsonify({
        'id': client.id,
        'username': client.username,
        'email': client.email,
        'phone': client.phone,
        'role': client.role
    }), 200


def update_client(client_id, data):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    client.username = data.get('username', client.username)
    client.email = data.get('email', client.email)
    client.phone = data.get('phone', client.phone)
    client.role = data.get('role', client.role)

    db.session.commit()
    return jsonify({'message': 'Client updated successfully'}), 200


def delete_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    db.session.delete(client)
    db.session.commit()
    return jsonify({'message': 'Client deleted successfully'}), 200
