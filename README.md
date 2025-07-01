# 🚀 Employee Attrition Prediction Web App

<div align="center">

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v3.0.3-green.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-v1.7.0-orange.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)

A modern, responsive Flask web application that predicts employee attrition using machine learning. Built with scikit-learn's RandomForestClassifier, this tool helps HR departments and managers identify employees at risk of leaving the organization.

[View Demo](#demo) · [Report Bug](https://github.com/krishnakamalbaishnab/Predict-Employee-Attrition-Using-this-Web-App/issues) · [Request Feature](https://github.com/krishnakamalbaishnab/Predict-Employee-Attrition-Using-this-Web-App/issues)

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🎯 Demo](#-demo)
- [🏗️ Architecture](#️-architecture)
- [⚡ Quick Start](#-quick-start)
- [🔧 Installation](#-installation)
- [📚 Usage](#-usage)
- [🤖 Model Information](#-model-information)
- [📁 Project Structure](#-project-structure)
- [🐳 Docker Deployment](#-docker-deployment)
- [🌐 Production Deployment](#-production-deployment)
- [🧪 Testing](#-testing)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [👨‍💻 Author](#-author)

## ✨ Features

- **🎯 Accurate Predictions**: Uses RandomForestClassifier with optimized hyperparameters
- **🖥️ Modern UI**: Clean, responsive web interface with real-time predictions
- **⚡ Fast Performance**: Efficient model loading and prediction pipeline
- **🔒 Input Validation**: Comprehensive form validation and error handling
- **📱 Mobile Friendly**: Responsive design that works on all devices
- **🚀 Easy Deployment**: Ready for production with Gunicorn and Docker support
- **📊 Feature Importance**: Understand which factors influence attrition most
- **🔧 Configurable**: Easy to retrain with new data

## 🎯 Demo

### Input Features
The model takes the following employee features:
- **Age**: Employee's age (18-65)
- **Monthly Income**: Salary in USD (1000-50000)
- **Years at Company**: Tenure in years (0-40)
- **Job Satisfaction**: Rating from 1-4 (1=Low, 4=High)
- **Work-Life Balance**: Rating from 1-4 (1=Poor, 4=Excellent)
- **Overtime**: Whether employee works overtime (0=No, 1=Yes)

### Example Prediction
```
📊 Sample Input:
Age: 35
Monthly Income: 5000
Years at Company: 8
Job Satisfaction: 2
Work-Life Balance: 1
Overtime: 1

🔮 Prediction: "The employee is predicted to leave."
```

## 🏗️ Architecture

```
┌─────────────┐    HTTP     ┌─────────────┐    joblib    ┌─────────────┐
│   Frontend  │ ──────────► │ Flask App   │ ───────────► │ ML Model    │
│ (HTML/CSS)  │             │ (Python)    │              │ (.pkl file) │
└─────────────┘             └─────────────┘              └─────────────┘
      ▲                           │                            │
      │                           ▼                            │
      └─────────── JSON Response ──────────────────────────────┘
```

## ⚡ Quick Start

```bash
# Clone the repository
git clone https://github.com/krishnakamalbaishnab/Predict-Employee-Attrition-Using-this-Web-App.git
cd Predict-Employee-Attrition-Using-this-Web-App

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open your browser and go to http://127.0.0.1:5000
```

## 🔧 Installation

### Prerequisites

- **Python 3.8+** (Tested with Python 3.8-3.12)
- **pip** (Python package installer)
- **Git** (for cloning the repository)

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/krishnakamalbaishnab/Predict-Employee-Attrition-Using-this-Web-App.git
   cd Predict-Employee-Attrition-Using-this-Web-App
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   python -c "import sklearn, flask, numpy; print('All dependencies installed successfully!')"
   ```

## 📚 Usage

### Running the Application

1. **Start the Flask Server**
   ```bash
   python app.py
   ```

2. **Access the Web Interface**
   - Open your browser
   - Navigate to `http://127.0.0.1:5000`
   - Fill in the employee details
   - Click "Predict" to get the attrition prediction

### API Usage

You can also use the prediction endpoint directly:

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -d "age=35&monthly_income=5000&years_at_company=8&job_satisfaction=2&work_life_balance=1&overtime=1"
```

## 🤖 Model Information

### Algorithm: Random Forest Classifier
- **Type**: Ensemble learning method
- **Features**: 6 input features
- **Output**: Binary classification (Stay=0, Leave=1)
- **Performance**: ~85% accuracy on test data

### Model Features
| Feature | Description | Range |
|---------|-------------|-------|
| Age | Employee age | 18-65 years |
| Monthly Income | Salary in USD | $1,000-$50,000 |
| Years at Company | Tenure | 0-40 years |
| Job Satisfaction | Satisfaction level | 1-4 (1=Low, 4=High) |
| Work-Life Balance | Balance rating | 1-4 (1=Poor, 4=Excellent) |
| Overtime | Overtime work | 0=No, 1=Yes |

### Retraining the Model

To retrain with new data:

```python
from sklearn.ensemble import RandomForestClassifier
import joblib
import pandas as pd

# Load your data
df = pd.read_csv('your_employee_data.csv')

# Prepare features and target
X = df[['age', 'monthly_income', 'years_at_company', 
        'job_satisfaction', 'work_life_balance', 'overtime']]
y = df['attrition']

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, 'model_current.pkl')
```

## 📁 Project Structure

```
Predict-Employee-Attrition-Using-this-Web-App/
├── 📄 app.py                 # Main Flask application
├── 📄 model_current.pkl      # Trained ML model
├── 📄 requirements.txt       # Python dependencies
├── 📄 LICENSE               # MIT License
├── 📄 README.md             # Project documentation
└── 📁 templates/
    └── 📄 index.html         # Web interface template
```

## 🐳 Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

Build and run:

```bash
docker build -t employee-attrition-app .
docker run -p 5000:5000 employee-attrition-app
```

## 🌐 Production Deployment

### Using Gunicorn

```bash
gunicorn --bind 0.0.0.0:8000 --workers 4 app:app
```

### Environment Variables

```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
```

## 🧪 Testing

Run tests to verify functionality:

```python
# test_app.py
import pytest
from app import app

def test_home_page():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_prediction():
    client = app.test_client()
    response = client.post('/predict', data={
        'age': '35',
        'monthly_income': '5000',
        'years_at_company': '8',
        'job_satisfaction': '2',
        'work_life_balance': '1',
        'overtime': '1'
    })
    assert response.status_code == 200
```

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/Predict-Employee-Attrition-Using-this-Web-App.git

# Install development dependencies
pip install -r requirements.txt
pip install pytest flask-testing

# Run tests
pytest
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Krishna Kamal Baishnab**
- GitHub: [@krishnakamalbaishnab](https://github.com/krishnakamalbaishnab)
- LinkedIn: [Connect with me](https://linkedin.com/in/krishnakamalbaishnab)

---

<div align="center">

### ⭐ Star this repository if you found it helpful!

Made with ❤️ by [Krishna Kamal Baishnab](https://github.com/krishnakamalbaishnab)

</div>
