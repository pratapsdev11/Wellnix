"""
Application routes
"""
import os
import logging
from datetime import datetime
from flask import Blueprint, render_template, request, url_for, Response
from muscle_ai.app.models.analyzer import MovementAnalyzer
from muscle_ai.app.models.yolo import get_yolo_models
from muscle_ai.app.utils.video import process_video

logger = logging.getLogger(__name__)
muscle_bp = Blueprint('muscle', __name__, template_folder='templates', static_folder='static')
models = get_yolo_models()

def register_routes(app):
    """Register all application routes"""
    global models
    models = get_yolo_models()
    @muscle_bp.route('/', methods=['GET', 'POST'])
    # @app.route('/', methods=['GET', 'POST'])
    def index():
        """Main page route with video upload form"""
        if request.method == 'POST':
            if 'video' not in request.files:
                return render_template('muscle_index.html', message='No video file uploaded')
            
            file = request.files['video']
            if file.filename == '':
                return render_template('muscle_index.html', message='No selected file')

            if not file.filename.lower().endswith(('.mp4', '.avi', '.mov')):
                return render_template('muscle_index.html', 
                                    message='Invalid file type. Please upload MP4, AVI, or MOV files')

            exercise_type = request.form.get('exercise_type')
            if exercise_type not in app.config['SUPPORTED_EXERCISES']:
                return render_template('muscle_index.html', message='Invalid exercise type')

            try:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                base_filename = os.path.splitext(file.filename)[0]
                filename = f"{timestamp}_{base_filename}"
                video_path = os.path.join(app.config['VIDEO_FOLDER'], filename)
                processed_path = os.path.join(app.config['PROCESSED_FOLDER'], 
                                            f'processed_{filename}.mp4')
                web_filename = f'web_{filename}.mp4'
                web_path = os.path.join(app.config['STATIC_FOLDER'], web_filename)
                
                file.save(video_path)
                
                metrics = process_video(
                    video_path, 
                    processed_path, 
                    web_path,
                    exercise_type, 
                    models[exercise_type]
                )
                
                # Clean up temporary files
                if os.path.exists(video_path):
                    os.remove(video_path)
                if os.path.exists(processed_path):
                    os.remove(processed_path)
                
                return render_template('muscle_index.html',
                                    video_url=url_for('muscle.static', filename=os.path.basename(web_path)),
                                    movement_analysis={
                                        'score': metrics['movement_assessment']['score'],
                                        'metrics': metrics
                                    })

            except Exception as e:
                logger.error(f"Error processing upload: {e}", exc_info=True)
                return render_template('muscle_index.html', message=f'Error processing video: {str(e)}')

        return render_template('muscle_index.html')
    @muscle_bp.route('/live', methods=['POST'])
    # @app.route('/live', methods=['POST'])
    def live():
        """Live streaming route"""
        exercise_type = request.form.get('live_exercise_type')
        if exercise_type not in app.config['SUPPORTED_EXERCISES']:
            return "Invalid exercise type", 400

        def generate_frames():
            """Generator function for streaming video frames"""
            import cv2
            import torch
            import numpy as np
            
            cap = cv2.VideoCapture(0)
            analyzer = MovementAnalyzer(exercise_type)
            yolo_model = models[exercise_type]
            use_gpu = torch.cuda.is_available()
            
            try:
                while True:
                    success, frame = cap.read()
                    if not success:
                        break

                    if use_gpu:
                        frame_tensor = torch.from_numpy(frame).cuda().half()
                        results = yolo_model(frame_tensor, stream=True)
                    else:
                        results = yolo_model(frame, stream=True)
                    
                    for result in results:
                        frame = result.orig_img
                        labels = {}
                        
                        if result.boxes is not None:
                            for box in result.boxes:
                                class_id = int(box.cls)
                                conf = float(box.conf)
                                label = result.names[class_id]
                                labels[label] = conf

                        form_value, down_value = analyzer.process_frame(labels)
                        
                        if hasattr(result, 'keypoints') and result.keypoints is not None:
                            keypoints = result.keypoints.xy[0]
                            for point in keypoints:
                                x, y = int(point[0]), int(point[1])
                                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

                        metrics = analyzer.get_metrics()
                        if metrics:
                            cv2.putText(frame, f"Score: {metrics['movement_assessment']['score']}/10",
                                      (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            cv2.putText(frame, f"Reps: {metrics['repetitions']}",
                                      (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            finally:
                cap.release()

        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')