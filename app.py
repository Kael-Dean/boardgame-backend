from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from auth_routes import auth_bp
from table_routes import table_bp

app = Flask(__name__)
app.config.from_object(Config)

# ✅ ตั้งค่า CORS ให้ถูกต้อง
CORS(app, resources={r"/api/*": {"origins": "https://boardgame-app-inky.vercel.app"}}, supports_credentials=True)

# Setup extensions
JWTManager(app)
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(table_bp, url_prefix='/api')

@app.route('/')
def index():
    return 'Backend is running 🎯'

if __name__ == '__main__':
    app.run(debug=True)
