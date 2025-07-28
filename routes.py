from flask import Blueprint
from controllers.auth_controller import register_user, login_user, logout_user
from controllers.order_controller import create_order, get_orders, get_order_by_id
from controllers.payments_controllers import create_payment, get_payment
from controllers.comment_controller import add_comment, get_comments_by_order
from middlewares.auth_middleware import login_required, roles_required

routes_bp = Blueprint('routes', __name__)

routes_bp.add_url_rule('/auth/register', view_func=register_user, methods=['POST'])
routes_bp.add_url_rule('/auth/login', view_func=login_user, methods=['POST'])
routes_bp.add_url_rule('/auth/logout', view_func=logout_user, methods=['POST'])

routes_bp.add_url_rule('/orders', view_func=login_required(get_orders), methods=['GET'])
routes_bp.add_url_rule('/orders', view_func=login_required(create_order), methods=['POST'])
routes_bp.add_url_rule('/orders/<int:order_id>', view_func=login_required(get_order_by_id), methods=['GET'])

routes_bp.add_url_rule('/payments', view_func=login_required(create_payment), methods=['POST'])
routes_bp.add_url_rule('/payments/<int:id>', view_func=login_required(get_payment), methods=['GET'])

routes_bp.add_url_rule('/comments', view_func=login_required(add_comment), methods=['POST'])
routes_bp.add_url_rule('/orders/<int:order_id>/comments', view_func=login_required(get_comments_by_order), methods=['GET'])
