from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from farend.models.comments import Comments
from farend.models.user import User
from farend.extensions import db
from farend.schema.comment_schema import commentschema, comments_schema

comment_bp = Blueprint('comments', __name__, url_prefix='/comments')

@comment_bp.route('/', methods=['GET'])
def get_comments():
    comments = Comments.query.order_by(Comments.created_at.desc()).all()
    return jsonify(comments_schema.dump(comments)), 200


@comment_bp.route('/', methods=['POST'])
@jwt_required()
def post_comment():
    user_id = get_jwt_identity()
    data = request.get_json()

    content = data.get('content')
    if not content:
        return jsonify({'error': 'Comment content is required'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    new_comment = Comments(
        content=content,
        user_id=user.id,
        username=user.username,
        created_at=datetime.utcnow()
    )

    db.session.add(new_comment)
    db.session.commit()

    return jsonify(commentschema.dump(new_comment)), 201
