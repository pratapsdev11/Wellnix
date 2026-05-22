# 🌌 Wellnix | AI-Powered Unified Health & Fitness Ecosystem
Welcome to **Wellnix**, a web ecosystem that bridges the gap between scientific nutrition tracking and advanced biomechanical fitness coaching. Wellnix brings two state-of-the-art artificial intelligence modules together under a beautifully designed, responsive Flask web application: **Nutri AI** (Health-O-Meter) and **Muscle AI** (JIM).
Whether scanning food packaging for personal health safety or analyzing training form down to individual joint coordinates, Wellnix provides immediate, data-driven, science-backed guidance to empower your wellness journey.
---
## 🌟 Key Pillars of Wellnix
### 🥦 1. Nutri AI (Health-O-Meter)
An intelligent food safety agent that reads food nutrition tables, calculates health indexes, and scores food items based on personal medical conditions, allergies, and the famous *Harvard Medical School Guide to Healthy Eating*.
*   **Intelligent OCR Label Scanning**: Integrates [EasyOCR](https://github.com/JaidedAI/EasyOCR) to read nutrient tables directly from photos or packaging.
*   **Profile-Based Metrics Calculation**: Automatically computes critical personal indexes including Body Mass Index (BMI), Basal Metabolic Rate (BMR), Daily Caloric Requirements, and safe nutrient thresholds.
*   **Groq Llama-3 RAG Agent**: Uses Retrieval-Augmented Generation (RAG) to scan reference medical guides and custom disease databases, calling the Groq Cloud API (`llama3-70b-8192`) to output a highly personalized **Consumability Score (0-100)** and evidence-backed eating recommendations.
### 🏋️ 2. Muscle AI (JIM)
A high-performance biomechanical computer vision platform that guides, scores, and tracks exercises in real-time, helping athletes avoid injuries and maximize muscle recruitment.
*   **YOLOv8 Posture & Form Detection**: Employs fine-tuned [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) models to track poses, depth, and form across six key major compounds:
    *   *Regular Deadlift*
    *   *Sumo Deadlift*
    *   *Conventional Squat*
    *   *Romanian Deadlift*
    *   *Zercher Squat*
    *   *Front Squat*
*   **Biomechanical Repetition Analyzer**: Leverages a robust state-machine posture detector that filters signal noise via a moving-average smoothing window, accurately counting reps and highlighting form flaws.
*   **Live Stream Core Processing**: Offers dual modes: high-fidelity pre-recorded video analysis and real-time live webcam processing with GPU acceleration.
---
---
## 🛠️ Installation & Getting Started
### 📋 Prerequisites
*   **Python**: Version `3.9` to `3.11` recommended.
*   **CUDA (Optional)**: CUDA Toolkit 11.8+ configured on Windows for maximum real-time camera inference speed.
### ⚙️ Steps
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/wellnix.git
    cd wellnix
    ```
2.  **Establish Virtual Environment & Install Requirements**
    On Windows:
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r heltin/health_o_meter/requirements.txt
    pip install ultralytics opencv-python
    ```
3.  **Download Custom Weights**
    Ensure your custom-trained YOLOv8 weights are saved inside the correct models directory:
    *   `heltin/muscle_ai/models/best.pt`
    *   `heltin/muscle_ai/models/sumo_best.pt`
    *   `heltin/muscle_ai/models/squats_best.pt`
    *   `heltin/muscle_ai/models/best_romanian.pt`
    *   `heltin/muscle_ai/models/zercher_best.pt`
    *   `heltin/muscle_ai/models/front_squats_best.pt`
4.  **Set Up Environment Variables**
    Create a `.env` file inside the `heltin/` directory:
    ```env
    GROQ_API_KEY=gsk_your_actual_groq_api_key_goes_here
    ```
5.  **Run the Portal!**
    ```bash
    cd heltin
    python app.py
    ```
    Open your browser and navigate to `http://localhost:5000` to start your balanced health journey!
---
## 🏆 Project Achievements & Impact
|
 Metric 
|
 Details 
|
|
:---
|
:---
|
|
**
Unified Portal
**
|
 Integrated 2 disparate Flask repos into 1 unified modular Blueprint architecture. 
|
|
**
High GPU Performance
**
|
 Implemented optional FP16 model compilation on CUDA to secure 30+ Webcam FPS. 
|
|
**
Evidence-based Scoring
**
|
 Successfully coupled EasyOCR outputs with a vector-indexed chunk library for Harvard Health guide compliance. 
|
|
**
Postural Precision
**
|
 Replaced rigid joint-angle heuristics with dynamic multi-state bounding label checks to prevent false counts. 
|
---
## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
All nutritional analysis is powered by the *Harvard Medical School Guide to Healthy Eating*. Gym posture analysis represents predictive guidelines, not clinical prescriptions. Make sure to consult with a physician before starting any intense weight-training routine.
