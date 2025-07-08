from flask import Blueprint, request, jsonify
from models import db, User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/sign-up', methods=['POST'])
def sign_up():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    age = data.get('age')

    # เช็คว่า email ซ้ำหรือยัง
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
        token = create_access_token(identity=str(user.id))  # 🔒 ใช้ str(user.id) เพื่อไม่ให้ JWT error
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username
            }
        }), 200

    return jsonify({'message': 'Invalid credentials'}), 401
