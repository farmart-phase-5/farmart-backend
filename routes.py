from flask import Blueprint, request, session
from .controllers.auth_controller import register_user, login_user, logout_user
from .controllers.order_controller import create_order, get_orders, get_order_by_id
from .controllers.payments_controllers import create_payment, get_payment
from .controllers.comment_controller import post_comment, get_comments
from .middlewares.auth_middleware import login_required

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/auth/register', methods=['POST'])
def register_route():
    data = request.get_json()
    return register_user(data)

@routes_bp.route('/auth/login', methods=['POST'])
def login_route():
    data = request.get_json()
    return login_user(data)

@routes_bp.route('/auth/logout', methods=['POST'])
@login_required
def logout_route():
    return logout_user()

@routes_bp.route('/orders', methods=['GET'])
@login_required
def get_orders_route():
    return get_orders()

@routes_bp.route('/orders', methods=['POST'])
@login_required
def create_order_route():
    data = request.get_json()
    return create_order(data)

@routes_bp.route('/orders/<int:order_id>', methods=['GET'])
@login_required
def get_order_by_id_route(order_id):
    return get_order_by_id(order_id)

@routes_bp.route('/payments', methods=['POST'])
@login_required
def create_payment_route():
    data = request.get_json()
    return create_payment(data) 

@routes_bp.route('/payments/<int:id>', methods=['GET'])
@login_required
def get_payment_route(id):
    return get_payment(id)

@routes_bp.route('/comments', methods=['POST'])
@login_required
def post_comment_route():
    data = request.get_json()
    user_id = session.get('user_id')
    return post_comment(user_id, data) 

@routes_bp.route('/orders/<int:order_id>/comments', methods=['GET'])
@login_required
def get_comments_route(order_id):
    return get_comments(order_id) 
