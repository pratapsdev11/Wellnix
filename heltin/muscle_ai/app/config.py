"""
Application configuration
"""
import os

class Config:
    """Application configuration settings"""
    # File paths
    VIDEO_FOLDER =  os.path.abspath(os.path.join(os.path.dirname(__file__),'videos'))
    PROCESSED_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__),'processed_videos'))
    STATIC_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__),'static'))
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Exercise types
    SUPPORTED_EXERCISES = [
        'regular_deadlift',
        'sumo_deadlift', 
        'squat',
        'romanian_deadlift',
        'zercher_squat',
        'front_squat'
    ]
    
    # Model paths
    # MODEL_PATHS = {
    #     'regular_deadlift': 'models/best.pt',
    #     'sumo_deadlift': 'models/sumo_best.pt',
    #     'squat': 'models/squats_best.pt',
    #     'romanian_deadlift': 'models/best_romanian.pt',
    #     'zercher_squat': 'models/zercher_best.pt',
    #     'front_squat': 'models/front_squats_best.pt'
    # }
    MODEL_PATHS = {
    'regular_deadlift': os.path.abspath('./muscle_ai/models/best.pt'),
    'sumo_deadlift': os.path.abspath('./muscle_ai/models/sumo_best.pt'),
    'squat': os.path.abspath('./muscle_ai/models/squats_best.pt'),
    'romanian_deadlift': os.path.abspath('./muscle_ai/models/best_romanian.pt'),
    'zercher_squat': os.path.abspath('./muscle_ai/models/zercher_best.pt'),
    'front_squat': os.path.abspath('./muscle_ai/models/front_squats_best.pt')
    }