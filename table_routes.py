from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, GameTable  # ✅ ใช้ชื่อใหม่

table_bp = Blueprint('table', __name__)

# GET /api/tables
@table_bp.route('/tables', methods=['GET'])
@jwt_required()
def get_tables():
    tables = GameTable.query.all()
    data = []
    for table in tables:
        data.append({
            'id': table.id,
            'name': table.name,
            'max_players': table.max_players,
            'current_players': len(table.users),
            'is_full': len(table.users) >= table.max_players,
            'members': [{'id': u.id, 'username': u.username} for u in table.users]
        })
    return jsonify({'tables': data})


# POST /api/join_table/<table_id>
@table_bp.route('/join_table/<int:table_id>', methods=['POST'])
@jwt_required()
def join_table(table_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    table = GameTable.query.get(table_id)

    if not table:
        return jsonify({'error': 'โต๊ะไม่พบ'}), 404

    # ลบ user ออกจากทุกโต๊ะก่อน (เข้าได้แค่ 1 โต๊ะ)
    for t in GameTable.query.all():
        if user in t.users:
            t.users.remove(user)

    if len(table.users) >= table.max_players:
        return jsonify({'error': 'โต๊ะเต็มแล้ว'}), 400

    table.users.append(user)
    db.session.commit()
    return jsonify({'message': 'เข้าร่วมโต๊ะสำเร็จ'})


# POST /api/leave_table/<table_id>
@table_bp.route('/leave_table/<int:table_id>', methods=['POST'])
@jwt_required()
def leave_table(table_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    table = GameTable.query.get(table_id)

    if not table or user not in table.users:
        return jsonify({'error': 'คุณไม่ได้อยู่ในโต๊ะนี้'}), 400

    table.users.remove(user)
    db.session.commit()
    return jsonify({'message': 'ออกจากโต๊ะแล้ว'})


# GET /api/table/<table_id>/members
@table_bp.route('/table/<int:table_id>/members', methods=['GET'])
@jwt_required()
def get_table_members(table_id):
    table = GameTable.query.get(table_id)
    if not table:
        return jsonify({'error': 'ไม่พบโต๊ะ'}), 404

    members = [{'id': u.id, 'username': u.username} for u in table.users]
    return jsonify(members)

# 👇 บรรทัดสุดท้าย
__all__ = ['table_bp']
