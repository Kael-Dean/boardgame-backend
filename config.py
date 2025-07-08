import os
from dotenv import load_dotenv

# โหลดตัวแปรจาก .env (ใช้ได้เฉพาะตอนรัน local)
load_dotenv()

class Config:
    # ✅ ใช้ DATABASE_URL จาก .env หรือ Environment Variable ของ Render
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    # ✅ ปิดการ track modifications เพื่อประสิทธิภาพ
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ ใช้ JWT_SECRET_KEY จาก .env หรือ Environment Variable
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
