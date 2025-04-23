"""
Initialize Flask application
"""
import logging
from flask import Flask
from muscle_ai.app.config import Config
from muscle_ai.app.routes import register_routes

logger = logging.getLogger(__name__)

def create_app(config_class=Config):
    """Create and configure the Flask application"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Register routes
    register_routes(app)
    
    logger.info("Flask application initialized")
    return app