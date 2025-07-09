from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from auth_routes import auth_bp
from table_routes import table_bp  # ✅ เพิ่มตรงนี้
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# ✅ CORS
CORS(app, resources={r"/api/*": {"origins": "https://boardgame-app-inky.vercel.app"}}, supports_credentials=True)

# ✅ Extensions
JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)

# ✅ Create tables (เฉพาะตอน local, ถ้า render จะไม่ใช้ตรงนี้)
with app.app_context():
    db.create_all()

# ✅ Blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(table_bp, url_prefix='/api')  # ✅ เพิ่มตรงนี้

@app.route('/')
def index():
    return 'Backend is running 🎯'

if __name__ == '__main__':
    app.run(debug=True)
