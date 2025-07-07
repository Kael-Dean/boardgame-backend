from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from auth_routes import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

# Setup extensions
CORS(app)
JWTManager(app)
db.init_app(app)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api')

# Root route for testing
@app.route('/')
def index():
    return 'Backend is running 🎯'

# Run the app (only in development)
if __name__ == '__main__':
    app.run(debug=True)
