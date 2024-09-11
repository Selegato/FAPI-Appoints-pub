from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Date
from sqlalchemy.orm import relationship
from src.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)    
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    user_name = Column(String, index=True)
    email = Column(String, index=True)
    phone_number = Column(String)
    specialization = Column(String)
    country_origin = Column(String)
    date_of_birth = Column(Date)
    is_active = Column(Boolean, default=True)

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    user_name = Column(String, index=True)
    email = Column(String, index=True)
    phone_number = Column(String)
    country_origin = Column(String)
    date_of_birth = Column(Date)
    is_active = Column(Boolean, default=True)

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    appointment_date = Column(Date)
    doctor = relationship("Doctor")
    patient = relationship("Patient")