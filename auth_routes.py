@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        token = create_access_token(identity=str(user.id))  # ✅ str() ปลอดภัยกว่า
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username
            }
        }), 200

    return jsonify({'message': 'Invalid credentials'}), 401
