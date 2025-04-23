# Health-O-Meter

Health-O-Meter is an intelligent system that analyzes food nutritional information and provides personalized consumability scores based on your health profile.

## Features

- **OCR Scanning**: Extract nutrition information from food packaging images
- **Health Profile Analysis**: Calculate BMI, BMR, and other health metrics
- **Personalized Scoring**: Generate a consumability score using GroqAI with RAG approach
- **Evidence-Based Recommendations**: Powered by "Eat, Drink, and Be Healthy: The Harvard Medical School Guide to Healthy Eating"

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/health-o-meter.git
cd health-o-meter
```

2. Create a virtual environment and install dependencies:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables:
```
cp .env.example .env
```
Edit the `.env` file and add your GroqAI API key.

4. Prepare the data:
- Make sure to preprocess the book chapters and save them in `data/book_chunks.json`
- Create reference data files in `data/diseases.json` and `data/nutrient_limits.json`

## Usage

1. Start the Flask application:
```
python interface/app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Follow the steps:
   - Enter your health profile
   - Upload a nutrition label image
   - View your personalized consumability score and recommendations

## Project Structure

```
health_o_meter/
│
├── ocr/                               # OCR module for nutrition table
├── user_profile/                      # User health info logic
├── data/                              # Static + reference data
├── scoring/                           # Core logic for scoring
├── retrieval/                         # RAG-related tools
├── interface/                         # Flask application
├── outputs/                           # Results & reports
├── utils/                             # Generic helpers
└── tests/                             # Unit tests
```

## Requirements

- Python 3.8+
- EasyOCR
- Flask
- GroqAI API access

## License

MIT License