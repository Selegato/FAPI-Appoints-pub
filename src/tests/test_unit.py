import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Doctor, Patient, Appointment
from src.database import Base
from datetime import date

# Configuração do banco de dados para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=engine)

    def setUp(self):
        self.db = TestingSessionLocal()

    def tearDown(self):
        self.db.close()

#begin of test_doctor

    def test_create_doctor(self):
        doctor = Doctor(
            first_name="John",
            last_name="Doe",
            user_name="johndoe",
            email="john.doe@example.com",
            phone_number="1234567890",
            specialization="Cardiology",
            country_origin="USA",
            date_of_birth= date(1980, 1, 1),
            is_active=True
        )
        self.db.add(doctor)
        self.db.commit()
        self.db.refresh(doctor)
        self.assertIsNotNone(doctor.id)

    def test_get_doctor(self):
        doctor = Doctor(
            first_name="John",
            last_name="Doe",
            user_name="johndoe",
            email="john.doe@example.com",
            phone_number="1234567890",
            specialization="Cardiology",
            country_origin="USA",
            date_of_birth= date(1980, 1, 1),
            is_active=True
        )
        self.db.add(doctor)
        self.db.commit()
        self.db.refresh(doctor)
        self.db_doctor = self.db.query(Doctor).filter(Doctor.id == doctor.id).first()
        self.assertIsNotNone(self.db_doctor)

    def test_update_doctor(self):
        doctor = Doctor(
            first_name="John",
            last_name="Doe",
            user_name="johndoe",
            email="john.doe@example.com",
            phone_number="1234567890",
            specialization="Cardiology",
            country_origin="USA",
            date_of_birth= date(1980, 1, 1),
            is_active=True
        )
        self.db.add(doctor)
        self.db.commit()
        self.db.refresh(doctor)
        self.db_doctor = self.db.query(Doctor).filter(Doctor.id == doctor.id).first()
        doctor_update = {
            "first_name": "Updated",
        }
        for key, value in doctor_update.items():
            setattr(self.db_doctor, key, value)
        self.db.commit()
        self.db.refresh(self.db_doctor)
        self.assertEqual(self.db_doctor.first_name, "Updated")

    def test_delete_doctor(self):
        doctor = Doctor(
            first_name="John",
            last_name="Doe",
            user_name="johndoe",
            email="john.doe@example.com",
            phone_number="1234567890",
            specialization="Cardiology",
            country_origin="USA",
            date_of_birth= date(1980, 1, 1),
            is_active=True
        )
        self.db.add(doctor)
        self.db.commit()
        self.db.refresh(doctor)
        self.db.delete(doctor)
        self.db.commit()
        self.db_doctor = self.db.query(Doctor).filter(Doctor.id == doctor.id).first()
        self.assertIsNone(self.db_doctor)

#end of test_doctor

    def test_create_patient(self):
            patient = Patient(
                first_name="Jane",
                last_name="Doe",
                user_name="janedoe",
                email="jane.doe@example.com",
                phone_number="0987654321",
                country_origin="USA",
                date_of_birth= date(1980, 1, 1),
                is_active=True
            )
            self.db.add(patient)
            self.db.commit()
            self.db.refresh(patient)
            self.assertIsNotNone(patient.id)

    def test_get_patient(self):
        patient = Patient(
            first_name="Jane",
            last_name="Doe",
            user_name="janedoe",
            email="jane.doe@example.com",
            phone_number="0987654321",
            country_origin="USA",
            date_of_birth=date(1990, 1, 1),
            is_active=True
        )
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        self.db_patient = self.db.query(Patient).filter(Patient.id == patient.id).first()
        self.assertIsNotNone(self.db_patient)

    def test_update_patient(self):
        patient = Patient(
            first_name="Jane",
            last_name="Doe",
            user_name="janedoe",
            email="jane.doe@example.com",
            phone_number="0987654321",
            country_origin="USA",
            date_of_birth=date(1990, 1, 1),
            is_active=True
        )
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        self.db_patient = self.db.query(Patient).filter(Patient.id == patient.id).first()
        
        # Campos a serem atualizados
        update_data = {
            "first_name": "Updated"
        }
        
        for key, value in update_data.items():
            setattr(self.db_patient, key, value)
        
        self.db.commit()
        self.db.refresh(self.db_patient)
        self.assertEqual(self.db_patient.first_name, "Updated")

    def test_delete_patient(self):
        patient = Patient(
            first_name="Jane",
            last_name="Doe",
            user_name="janedoe",
            email="jane.doe@example.com",
            phone_number="0987654321",
            country_origin="USA",
            date_of_birth=date(1990, 1, 1),
            is_active=True
        )
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        self.db.delete(patient)
        self.db.commit()
        self.db_patient = self.db.query(Patient).filter(Patient.id == patient.id).first()
        self.assertIsNone(self.db_patient)


#end of test_patient

    def test_create_appointment(self):
        doctor = Doctor(
            first_name="John",
            last_name="Doe",
            user_name="johndoe",
            email="john.doe@example.com",
            phone_number="1234567890",
            specialization="Cardiology",
            country_origin="USA",
            date_of_birth= date(1980, 1, 1),
            is_active=True
        )
        patient = Patient(
            first_name="Jane",
            last_name="Doe",
            user_name="janedoe",
            email="jane.doe@example.com",
            phone_number="0987654321",
            country_origin="USA",
            date_of_birth= date(1980, 1, 1),
            is_active=True
        )
        self.db.add(doctor)
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(doctor)
        self.db.refresh(patient)

        appointment = Appointment(
            doctor_id=doctor.id,
            patient_id=patient.id,
            appointment_date= date(1980, 1, 1),
        )
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        self.assertIsNotNone(appointment.id)

    def test_get_appointment(self):
        appointment = Appointment(
            doctor_id=1,
            patient_id=1,
            appointment_date=date(2023, 10, 1),
        )
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        self.db_appointment = self.db.query(Appointment).filter(Appointment.id == appointment.id).first()
        self.assertIsNotNone(self.db_appointment)

    def test_update_appointment(self):
        appointment = Appointment(
            doctor_id=1,
            patient_id=1,
            appointment_date=date(2023, 10, 1),
        )
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        self.db_appointment = self.db.query(Appointment).filter(Appointment.id == appointment.id).first()
        
        # Campos a serem atualizados
        update_data = {
            "doctor_id": 2
        }
        
        for key, value in update_data.items():
            setattr(self.db_appointment, key, value)
        
        self.db.commit()
        self.db.refresh(self.db_appointment)
        self.assertEqual(self.db_appointment.doctor_id, 2)

    def test_delete_appointment(self):
        appointment = Appointment(
            doctor_id=1,
            patient_id=1,
            appointment_date=date(2023, 10, 1),
        )
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        self.db.delete(appointment)
        self.db.commit()
        self.db_appointment = self.db.query(Appointment).filter(Appointment.id == appointment.id).first()
        self.assertIsNone(self.db_appointment)


if __name__ == '__main__':
    unittest.main()