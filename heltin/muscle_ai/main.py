#!/usr/bin/env python3
"""
JIM - AI Fitness Form Analysis Application
Main entry point for the application
"""
import os
import logging
from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('app.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Create required directories
def ensure_directories():
    """Ensure all required directories exist"""
    dirs = ['videos', 'processed_videos', 'static']
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
    logger.info("Directories initialized")

if __name__ == '__main__':
    # Ensure all required directories exist
    ensure_directories()
    
    # Create and run the Flask application
    app = create_app()
    logger.info("Starting JIM application...")
    app.run(debug=True)