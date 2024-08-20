from flask import Flask, request, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load the pre-trained model (make sure model_current.pkl is in the same directory as app.py)
model = joblib.load('model_current.pkl')

# Home route to render input form
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Assume the form inputs are passed as a list of values
        input_features = [float(x) for x in request.form.values()]
        input_array = np.array([input_features])
        
        # Predict using the loaded model
        prediction = model.predict(input_array)[0]
        
        # Generate a descriptive message based on the prediction
        if prediction == 0:
            result_message = "The employee is predicted to stay."
        else:
            result_message = "The employee is predicted to leave."
        
        # Display prediction result in the same form page
        return render_template('index.html', prediction_text=result_message)
    
    except Exception as e:
        return render_template('index.html', prediction_text=f'Error: {str(e)}')

if __name__ == "__main__":
    app.run(debug=True)
