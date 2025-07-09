from app import app
from models import db, GameTable  # ← ใช้ชื่อใหม่

with app.app_context():
    db.create_all()

    if GameTable.query.count() == 0:
        for i in range(1, 7):
            table = GameTable(name=f"โต๊ะที่ {i}", max_players=4)
            db.session.add(table)
        db.session.commit()
        print("✅ สร้างโต๊ะเรียบร้อยแล้ว")
    else:
        print("📦 โต๊ะมีอยู่แล้วในระบบ")
