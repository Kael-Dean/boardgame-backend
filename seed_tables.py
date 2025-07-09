from app import app
from models import db, Table

# ต้อง run ใน context ของ Flask
with app.app_context():
    for i in range(1, 7):  # สร้างโต๊ะ 1 ถึง 6
        table = Table(id=i, max_players=4)
        db.session.add(table)
    db.session.commit()
    print("✅ โต๊ะถูกสร้างเรียบร้อยแล้ว")
