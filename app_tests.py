from mockito import mock, verify
import unittest

from app import app

class AppTest(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
    
    def tearDown(self):
        self.ctx.pop()
    
    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert 'Generate a challan' in response.get_data(as_text=True)

    def test_about(self):
        response = self.client.get("/about")
        assert response.status_code == 200
        assert 'Web application for generating challans' in response.get_data(as_text=True)

    def test_generate_challan(self):
        response = self.client.post("/", 
                                    data=dict(vehicle_number='TS07HR9552', unit_name='Cyberabad',
                                              date = '06-Mar-2023', time='08:34', 
                                              place_of_violation = 'SUTHARIGUDA ORR', ps_limits = 'Alwal Tr PS',
                                              violation = 'Over speeding/ Dangerous Driving', fine_amount = 1000
                                               ))
        assert response.status_code == 302        
