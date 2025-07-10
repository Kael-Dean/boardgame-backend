from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ✅ ตารางกลาง User <-> GameTable
table_user = db.Table(
    'table_user',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('table_id', db.Integer, db.ForeignKey('game_tables.id'))
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer)

    # ✅ ความสัมพันธ์กับโต๊ะ
    tables = db.relationship('GameTable', secondary=table_user, backref='users')

class GameTable(db.Model):
    __tablename__ = 'game_tables'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    max_players = db.Column(db.Integer, default=4)
