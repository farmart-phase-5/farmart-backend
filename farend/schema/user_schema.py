from farend.models.user import User

class UserSchema:
    def __init__(self, data = None):
        self.data = data or {}
        self.error = []
        self.validated_data = {}

def validate_user_data(data): 
    errors = []
    validated_data = {}

    username = data.get('username')
    if not username:
        errors.append("Username is required and cannot be empty.")
    elif len(username) < 3:
        errors.append("Username must be at least 3 characters long.")
    else:
        validated_data['username'] = username

    email = data.get('email')
    if not email:
        errors.append("Email is required.")
    else:
        validated_data['email'] = email
        if User.query.filter_by(email=email).first():
            errors.append("Email already exists.")

    password = data.get('password')
    if not password:
        errors.append("Password is required.")
    elif len(password) < 6:
        errors.append("Password must be at least 6 characters long.")
    else:
        validated_data['password'] = password

    role = data.get('role', 'client')
    if role not in ['client', 'farmer', 'admin']:
        errors.append("Role must be 'client', 'farmer', or 'admin'.")
    validated_data['role'] = role

    return validated_data, errors

def serialize_user(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    }

def serialize_users(self,users):
    return [serialize_user(user) for user in users]