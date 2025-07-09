from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Table


table_bp = Blueprint('table', __name__)

# GET /api/tables
@table_bp.route('/tables', methods=['GET'])
@jwt_required()
def get_tables():
    tables = Table.query.all()
    data = []
    for table in tables:
        data.append({
            'id': table.id,
            'status': table.status,
            'members': [{'id': u.id, 'username': u.username} for u in table.members]
        })
    return jsonify({'tables': data})


# POST /api/join_table/<table_id>
@table_bp.route('/join_table/<int:table_id>', methods=['POST'])
@jwt_required()
def join_table(table_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    table = Table.query.get(table_id)

    if not table:
        return jsonify({'error': 'โต๊ะไม่พบ'}), 404

    # ลบ user จากทุกโต๊ะก่อน (เข้าได้แค่ 1 โต๊ะ)
    for t in Table.query.all():
        if user in t.members:
            t.members.remove(user)

    if len(table.members) >= table.max_players:
        return jsonify({'error': 'โต๊ะเต็มแล้ว'}), 400

    table.members.append(user)
    db.session.commit()
    return jsonify({'message': 'เข้าร่วมโต๊ะสำเร็จ'})


# POST /api/leave_table/<table_id>
@table_bp.route('/leave_table/<int:table_id>', methods=['POST'])
@jwt_required()
def leave_table(table_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    table = Table.query.get(table_id)

    if not table or user not in table.members:
        return jsonify({'error': 'คุณไม่ได้อยู่ในโต๊ะนี้'}), 400

    table.members.remove(user)
    db.session.commit()
    return jsonify({'message': 'ออกจากโต๊ะแล้ว'})


# GET /api/table/<table_id>/members
@table_bp.route('/table/<int:table_id>/members', methods=['GET'])
@jwt_required()
def get_table_members(table_id):
    table = Table.query.get(table_id)
    if not table:
        return jsonify({'error': 'ไม่พบโต๊ะ'}), 404

    members = [{'id': u.id, 'username': u.username} for u in table.members]
    return jsonify(members)

# 👇 เพิ่มบรรทัดนี้ท้ายสุด
__all__ = ['table_bp']
