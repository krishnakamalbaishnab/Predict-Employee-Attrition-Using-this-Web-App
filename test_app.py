"""
Simple tests for the Employee Attrition Prediction Flask App
"""
import unittest
import json
from app import app

class TestEmployeeAttritionApp(unittest.TestCase):
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        """Test if home page loads successfully"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'PREDICT EMPLOYEE ATTRITION', response.data)

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

    def test_prediction_valid_input(self):
        """Test prediction with valid input"""
        response = self.app.post('/predict', data={
            'age': '35',
            'monthly_income': '5000',
            'years_at_company': '8',
            'job_satisfaction': '2',
            'work_life_balance': '1',
            'overtime': '1'
        })
        self.assertEqual(response.status_code, 200)
        # Should contain either "STAY" or "LEAVE" in the response
        self.assertTrue(b'STAY' in response.data or b'LEAVE' in response.data)

    def test_prediction_invalid_input(self):
        """Test prediction with invalid input"""
        response = self.app.post('/predict', data={
            'age': '150',  # Invalid age
            'monthly_income': '5000',
            'years_at_company': '8',
            'job_satisfaction': '2',
            'work_life_balance': '1',
            'overtime': '1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error:', response.data)

    def test_api_prediction_valid(self):
        """Test API prediction with valid JSON input"""
        response = self.app.post('/api/predict', 
                                json={
                                    'age': 35,
                                    'monthly_income': 5000,
                                    'years_at_company': 8,
                                    'job_satisfaction': 2,
                                    'work_life_balance': 1,
                                    'overtime': 1
                                },
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('prediction', data)
        self.assertIn('confidence', data)

    def test_api_prediction_missing_field(self):
        """Test API prediction with missing field"""
        response = self.app.post('/api/predict', 
                                json={
                                    'age': 35,
                                    'monthly_income': 5000,
                                    # Missing other required fields
                                },
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('error', data)

    def test_404_error(self):
        """Test 404 error handling"""
        response = self.app.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main() 