from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from auth_routes import auth_bp
from table_routes import table_bp

app = Flask(__name__)
app.config.from_object(Config)

# ✅ CORS ปรับให้ครอบคลุม headers และ methods
CORS(app, resources={r"/api/*": {
    "origins": [
        "https://boardgame-app-inky.vercel.app",
        "http://localhost:5173"
    ],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}}, supports_credentials=True)

# ✅ JWT & DB
JWTManager(app)
db.init_app(app)

# ✅ Create tables (เฉพาะ local เท่านั้น)
with app.app_context():
    db.create_all()

# ✅ Blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(table_bp, url_prefix='/api')

@app.route('/')
def index():
    return 'Backend is running 🚀'

if __name__ == '__main__':
    app.run(debug=True)
