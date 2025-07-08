from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Table

table_bp = Blueprint('table', __name__)

@table_bp.route('/join_table/<int:table_id>', methods=["POST"])
@jwt_required()
def join_table(table_id):
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    table = Table.query.get_or_404(table_id)

    if user.tables:
        return jsonify({'error': 'User already in a table'}), 403

    user.tables.append(table)
    db.session.commit()
    return jsonify({'message': f'Joined table {table_id} successfully'}), 200


@table_bp.route('/leave_table/<int:table_id>', methods=["POST"])
@jwt_required()
def leave_table(table_id):
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    table = Table.query.get_or_404(table_id)

    if table not in user.tables:
        return jsonify({'error': 'User not in this table'}), 400

    user.tables.remove(table)
    db.session.commit()
    return jsonify({'message': f'Left table {table_id} successfully'}), 200


@table_bp.route('/table/<int:table_id>/members', methods=["GET"])
@jwt_required()
def table_members(table_id):
    table = Table.query.get_or_404(table_id)
    members = table.members

    member_data = [{'id': m.id, 'username': m.username, 'age': m.age} for m in members]
    return jsonify(member_data), 200
