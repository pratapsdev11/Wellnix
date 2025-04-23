import os
import json
from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from werkzeug.utils import secure_filename
import requests
from dotenv import load_dotenv

# Import project modules
from ocr.nutrition_extractor import extract_nutrition_info, parse_nutrition_table
from user_profile.process_profile import calculate_health_metrics
from scoring.consumability_agent import generate_consumability_score

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # Process profile data
        profile_data = {
            "age": int(request.form.get('age')),
            "gender": request.form.get('gender'),
            "height_cm": float(request.form.get('height_cm')),
            "weight_kg": float(request.form.get('weight_kg')),
            "activity_level": request.form.get('activity_level'),
            "diet_type": request.form.get('diet_type'),
            "goal": request.form.get('goal'),
            "smoker": request.form.get('smoker') == 'true',
            "alcohol_consumption": request.form.get('alcohol_consumption'),
            "allergies": request.form.get('allergies').split(',') if request.form.get('allergies') else [],
            "medical_history": {
                "diseases": json.loads(request.form.get('diseases', '[]')),
                "family_history": request.form.get('family_history').split(',') if request.form.get('family_history') else []
            },
            "food_preferences": {
                "cuisine": request.form.get('cuisine').split(',') if request.form.get('cuisine') else [],
                "spice_tolerance": request.form.get('spice_tolerance'),
                "meal_frequency": int(request.form.get('meal_frequency'))
            },
            "hydration_level": request.form.get('hydration_level'),
            "sleep_hours": float(request.form.get('sleep_hours')),
            "stress_level": request.form.get('stress_level')
        }
        
        # Save profile to session
        session['user_profile'] = profile_data
        
        # Calculate health metrics like BMI, BMR, etc.
        health_metrics = calculate_health_metrics(profile_data)
        session['health_metrics'] = health_metrics
        
        return redirect(url_for('upload_nutrition'))
    
    return render_template('profile.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_nutrition():
    if request.method == 'POST':
        # Check if file part exists
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract nutrition info using OCR
            try:
                extracted_text = extract_nutrition_info(filepath)
                nutrition_info = parse_nutrition_table(extracted_text)
                
                # Save nutrition info to session
                session['nutrition_info'] = nutrition_info
                
                return redirect(url_for('results'))
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    
    return render_template('upload.html')

@app.route('/results')
def results():
    # Check if we have all required data
    if 'user_profile' not in session or 'nutrition_info' not in session:
        return redirect(url_for('index'))
    
    user_profile = session['user_profile']
    nutrition_info = session['nutrition_info']
    health_metrics = session.get('health_metrics', {})
    
    # Generate consumability score using GroqAI and RAG approach
    score, explanation = generate_consumability_score(
        user_profile, 
        nutrition_info, 
        health_metrics, 
        api_key=GROQ_API_KEY
    )
    
    # Store the result
    result = {
        'user_profile': user_profile,
        'nutrition_info': nutrition_info,
        'health_metrics': health_metrics,
        'consumability_score': score,
        'explanation': explanation
    }
    
    # Save result to outputs folder with timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    os.makedirs('outputs', exist_ok=True)
    with open(f'outputs/result_{timestamp}.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    return render_template('results.html', 
                          score=score,
                          explanation=explanation, 
                          nutrition=nutrition_info,
                          health_metrics=health_metrics)

if __name__ == '__main__':
    app.run(debug=True)