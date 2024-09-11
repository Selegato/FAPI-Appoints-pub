from pydantic import BaseModel
from datetime import date

class Doctor(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    email: str
    phone_number: str
    specialization: str
    country_origin: str
    date_of_birth: date
    is_active: bool = True

class DoctorResponse(Doctor):
    id: int

    class Config:
        from_attributes = True

class Patient(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    email: str
    phone_number: str
    country_origin: str
    date_of_birth: date
    is_active: bool = True

class PatientResponse(Patient):
    id: int

    class Config:
        from_attributes = True

class Appointment(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_date: date

class AppointmentResponse(Appointment):
    id: int

    class Config:
        from_attributes = True