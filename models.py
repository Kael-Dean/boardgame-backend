from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ความสัมพันธ์ระหว่าง User และ Table (many-to-many)พะ

table_user = db.Table('table_user',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('table_id', db.Integer, db.ForeignKey('tables.id'))
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=True)

    # เพิ่มตรงนี้เพื่อดูว่า user คนนี้อยู่ในโต๊ะไหนบ้าง
    tables = db.relationship('Table', secondary=table_user, backref='members')

class Table(db.Model):
    __tablename__ = 'tables'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False, default="available")
