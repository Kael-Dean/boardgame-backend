from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from auth_routes import auth_bp
from table_routes import table_bp  # ✅ เพิ่ม blueprint สำหรับ table

app = Flask(__name__)
app.config.from_object(Config)

# ✅ Setup extensions
CORS(app, origins=["https://boardgame-app-inky.vercel.app"], supports_credentials=True)
JWTManager(app)
db.init_app(app)

# ✅ Create database tables if they don't exist
with app.app_context():
    db.create_all()

# ✅ Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(table_bp, url_prefix='/api')  # ✅ ครบถ้วน

# ✅ Root route for testing
@app.route('/')
def index():
    return 'Backend is running 🎯'

# ✅ Run the app (only in development)
if __name__ == '__main__':
    app.run(debug=True)
