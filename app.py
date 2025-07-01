import os
import logging
from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['ENV'] = os.environ.get('FLASK_ENV', 'development')

# Load the pre-trained model
MODEL_PATH = 'model_current.pkl'
try:
    model = joblib.load(MODEL_PATH)
    logger.info(f"Model loaded successfully from {MODEL_PATH}")
except FileNotFoundError:
    logger.error(f"Model file {MODEL_PATH} not found!")
    model = None
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    model = None

# Feature validation ranges
FEATURE_RANGES = {
    'age': (18, 65),
    'monthly_income': (1000, 50000),
    'years_at_company': (0, 40),
    'job_satisfaction': (1, 4),
    'work_life_balance': (1, 4),
    'overtime': (0, 1)
}

def validate_input(features):
    """
    Validate input features against expected ranges.
    
    Args:
        features (list): List of feature values
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if len(features) != 6:
        return False, "Expected 6 features, got {}".format(len(features))
    
    feature_names = ['age', 'monthly_income', 'years_at_company', 
                    'job_satisfaction', 'work_life_balance', 'overtime']
    
    for i, (name, value) in enumerate(zip(feature_names, features)):
        min_val, max_val = FEATURE_RANGES[name]
        if not (min_val <= value <= max_val):
            return False, f"{name.replace('_', ' ').title()} must be between {min_val} and {max_val}"
    
    return True, None

@app.route('/')
def home():
    """Render the main page with input form."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle prediction requests.
    
    Returns:
        Rendered template with prediction result or error message
    """
    if model is None:
        error_msg = "Model not available. Please check server configuration."
        logger.error(error_msg)
        return render_template('index.html', prediction_text=f'Error: {error_msg}')
    
    try:
        # Extract and validate form data
        form_values = list(request.form.values())
        
        if len(form_values) != 6:
            error_msg = f"Expected 6 input fields, received {len(form_values)}"
            return render_template('index.html', prediction_text=f'Error: {error_msg}')
        
        # Convert to float and validate
        try:
            input_features = [float(x) for x in form_values]
        except ValueError as e:
            error_msg = "All inputs must be valid numbers"
            return render_template('index.html', prediction_text=f'Error: {error_msg}')
        
        # Validate feature ranges
        is_valid, validation_error = validate_input(input_features)
        if not is_valid:
            return render_template('index.html', prediction_text=f'Error: {validation_error}')
        
        # Make prediction
        input_array = np.array([input_features])
        prediction = model.predict(input_array)[0]
        prediction_proba = model.predict_proba(input_array)[0]
        
        # Generate result message
        if prediction == 0:
            result_message = f"🟢 The employee is predicted to STAY (Confidence: {prediction_proba[0]:.1%})"
        else:
            result_message = f"🔴 The employee is predicted to LEAVE (Confidence: {prediction_proba[1]:.1%})"
        
        logger.info(f"Prediction made: {prediction} with confidence: {max(prediction_proba):.3f}")
        
        return render_template('index.html', prediction_text=result_message)
    
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        logger.error(error_msg)
        return render_template('index.html', prediction_text=f'Error: {error_msg}')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    API endpoint for prediction requests.
    
    Returns:
        JSON response with prediction result
    """
    if model is None:
        return jsonify({
            'error': 'Model not available',
            'success': False
        }), 500
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No JSON data provided',
                'success': False
            }), 400
        
        # Extract features
        required_fields = ['age', 'monthly_income', 'years_at_company', 
                          'job_satisfaction', 'work_life_balance', 'overtime']
        
        input_features = []
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'success': False
                }), 400
            input_features.append(float(data[field]))
        
        # Validate input
        is_valid, validation_error = validate_input(input_features)
        if not is_valid:
            return jsonify({
                'error': validation_error,
                'success': False
            }), 400
        
        # Make prediction
        input_array = np.array([input_features])
        prediction = model.predict(input_array)[0]
        prediction_proba = model.predict_proba(input_array)[0]
        
        return jsonify({
            'prediction': int(prediction),
            'prediction_text': 'stay' if prediction == 0 else 'leave',
            'confidence': float(max(prediction_proba)),
            'probabilities': {
                'stay': float(prediction_proba[0]),
                'leave': float(prediction_proba[1])
            },
            'success': True
        })
    
    except Exception as e:
        logger.error(f"API prediction error: {str(e)}")
        return jsonify({
            'error': f'Prediction failed: {str(e)}',
            'success': False
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'environment': app.config['ENV']
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('index.html', 
                         prediction_text='Error: Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return render_template('index.html', 
                         prediction_text='Error: Internal server error'), 500

if __name__ == "__main__":
    # Run the app
    debug_mode = app.config['ENV'] == 'development'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    
    logger.info(f"Starting Flask app on {host}:{port} (Debug: {debug_mode})")
    app.run(host=host, port=port, debug=debug_mode)
