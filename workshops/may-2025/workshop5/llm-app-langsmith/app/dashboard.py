from flask import Flask, render_template, jsonify
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import statistics

app = Flask(__name__)

def load_feedback_data() -> List[Dict[str, Any]]:
    """Load all feedback data from JSON files."""
    feedback_dir = Path("feedback")
    feedback_data = []
    
    for feedback_file in feedback_dir.glob("feedback_*.json"):
        try:
            with open(feedback_file, 'r') as f:
                data = json.load(f)
                feedback_data.append(data)
        except Exception as e:
            print(f"Error loading {feedback_file}: {e}")
    
    return sorted(feedback_data, key=lambda x: x['timestamp'])

def calculate_metrics(feedback_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate aggregate metrics from feedback data."""
    if not feedback_data:
        return {
            "total_responses": 0,
            "average_rating": 0,
            "response_times": [],
            "ratings": []
        }
    
    ratings = [f['rating'] for f in feedback_data]
    response_times = [f.get('evaluation_metrics', {}).get('response_length', 0) for f in feedback_data]
    
    return {
        "total_responses": len(feedback_data),
        "average_rating": statistics.mean(ratings) if ratings else 0,
        "response_times": response_times,
        "ratings": ratings
    }

@app.route('/')
def index():
    """Render the main dashboard page."""
    feedback_data = load_feedback_data()
    metrics = calculate_metrics(feedback_data)
    
    return render_template('dashboard.html',
                         feedback_data=feedback_data,
                         metrics=metrics)

@app.route('/api/metrics')
def get_metrics():
    """API endpoint for metrics data."""
    feedback_data = load_feedback_data()
    metrics = calculate_metrics(feedback_data)
    return jsonify(metrics)

@app.route('/api/feedback')
def get_feedback():
    """API endpoint for feedback data."""
    feedback_data = load_feedback_data()
    return jsonify(feedback_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 