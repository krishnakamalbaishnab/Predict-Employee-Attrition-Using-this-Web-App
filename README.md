
# Employee Attrition Prediction Flask App

This is a Flask web application that predicts employee attrition based on several input features such as age, monthly income, years at the company, job satisfaction, work-life balance, and whether the employee works overtime. The prediction is powered by a machine learning model trained using `scikit-learn`.

## Features

- Predict whether an employee will stay or leave (attrition) based on user input.
- Simple web interface built with Flask.
- Machine learning model trained using RandomForestClassifier from `scikit-learn`.

## Installation

### Prerequisites

- Python 3.x
- `pip` (Python package installer)
- Virtual environment setup (optional but recommended)

### Setup

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/krishnakamalbaishnab/Predict-Employee-Attrition-Using-this-Web-App.git
   cd your-repo-name
   
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Ensure that the trained model (`model_current.pkl`) is in the root directory of the project.

## Usage

1. Run the Flask app:

   ```bash
   python app.py
   ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

3. Enter the employee details (age, monthly income, etc.) and submit the form to get a prediction.

4. The app will display a message indicating whether the employee is predicted to stay or leave.

## Project Structure

```
.
├── app.py                  # Flask app code
├── model_current.pkl        # Trained model file
├── requirements.txt         # List of required Python packages
├── templates
│   └── index.html           # HTML template for the web app
└── README.md                # Project documentation
```

## Model Training

The model was trained using a synthetic dataset that includes features like age, monthly income, years at the company, job satisfaction, work-life balance, and overtime status. The model used is a RandomForestClassifier from `scikit-learn`.

To retrain the model, use the provided script:

```bash
python retrain_model.py
```

This will generate a new `model_current.pkl` file which can be used by the Flask app.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
