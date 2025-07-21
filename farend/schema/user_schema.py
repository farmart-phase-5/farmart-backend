from farend.models.user import User

def validate_user_data(data): 
    errors = []
    validated_data = {}

    if 'username' not in data or not data['username']:
        errors.append("Username is required and cannot be empty.")
    elif len(data['username']) < 3:
        errors.append("Username must be at least 3 characters long.")
    else:
        validated_data['username'] = data['username']

    if 'email' not in data or not data['email']:
        errors.append("Email is required.")
    else:
        validated_data['email'] = data['email']
        if User.query.filter_by(email=data['email']).first():
            errors.append("Email already exists.")

    if 'password' not in data or not data['password']:
        errors.append("Password is required.")
    elif len(data['password']) < 6:
        errors.append("Password must be at least 6 characters long.")
    else:
        validated_data['password'] = data['password']

    if 'role' in data and data['role'] not in ['client', 'farmer', 'admin']:
        errors.append("Role must be 'client', 'farmer', or 'admin'.")
    else:
        validated_data['role'] = data.get('role', 'client')

    return validated_data, errors

def serialize_user(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    }

def serialize_users(users):
    return [serialize_user(user) for user in users]