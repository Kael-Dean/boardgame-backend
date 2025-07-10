from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from models import db, User

auth_bp = Blueprint('auth', __name__)  # ✅ ต้องมาก่อนใช้ route
bcrypt = Bcrypt()

@auth_bp.route('/sign-up', methods=['POST'])
def sign_up():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    age = data.get('age')

    # ตรวจซ้ำ
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(email=email, username=username, password=hashed_pw, age=age)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Signup success'}), 200


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        token = create_access_token(identity=str(user.id))
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username
            }
        }), 200

    return jsonify({'message': 'Invalid credentials'}), 401
