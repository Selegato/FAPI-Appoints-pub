import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base, get_db
from main import app
from src.models import Doctor, Patient, Appointment
from datetime import date

# TEST DATABASE
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# OVERRIDE DATABASE FOR TEST
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=engine)

    def setUp(self):
        self.db = TestingSessionLocal()

    def tearDown(self):
        self.db.close()

    def test_add_doctor(self):
        doctor_data = {
            "first_name": "string",
            "last_name": "string",
            "user_name": "string",
            "email": "string",
            "phone_number": "string",
            "specialization": "string",
            "country_origin": "string",
            "date_of_birth": "2024-09-11",
            "is_active": True
        }
        response = self.client.post("/api/doctors/", json=doctor_data)
        self.assertEqual(response.status_code, 200)

    def test_add_patient(self):
        patient_data = {
            "first_name": "string",
            "last_name": "string",
            "user_name": "string",
            "email": "string",
            "phone_number": "string",
            "country_origin": "string",
            "date_of_birth": "2024-09-11",
            "is_active": True
        }
        response = self.client.post("/api/patients/", json=patient_data)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()