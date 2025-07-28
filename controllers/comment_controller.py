from flask import jsonify
from ..extensions import db
from ..models.comments import Comments
from ..models.user import User

def post_comment(user_id, data):
    content = data.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400

    comment = Comments(content=content, user_id=user_id)
    db.session.add(comment)
    db.session.commit()

    return jsonify({'message': 'Comment posted'}), 201

def get_comments():
    comments = Comments.query.all()
    result = []
    for comment in comments:
        user = User.query.get(comment.user_id)
        result.append({
            'id': comment.id,
            'content': comment.content,
            'username': user.username if user else 'Unknown'
        })
    return jsonify(result), 200
