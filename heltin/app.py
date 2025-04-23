from flask import Flask, render_template
from health_o_meter.app import health_bp
from muscle_ai.app.routes import muscle_bp, register_routes
from muscle_ai.app.config import Config
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object(Config)
# Register muscle routes
register_routes(app)
# Create video directories if they don't exist
os.makedirs(app.config['VIDEO_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)
# Register Blueprints
app.register_blueprint(health_bp, url_prefix='/health')
app.register_blueprint(muscle_bp, url_prefix='/muscle')

@app.route('/')
def home():
    """Home page for the unified web app."""
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)