from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from src import schemas, models
from datetime import date

router = APIRouter()




@router.get("/appointments/", response_model=List[schemas.AppointmentResponse])
def get_appointments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_appointments = db.query(models.Appointment).offset(skip).limit(limit).all()
    if not db_appointments:
        raise HTTPException(status_code=404, detail="No appointments found")
    return db_appointments

@router.get("/appointments/{appointment_id}", response_model=schemas.AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment

@router.post("/appointments/", response_model=schemas.AppointmentResponse)
def add_appointment(doctor_id: int, patient_id: int, appointment_date: date, db: Session = Depends(get_db)):
    doctor_exists = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor_exists:
        raise HTTPException(status_code=404, detail="Doctor not found")

    patient_exists = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient_exists:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db_appointment = models.Appointment(doctor_id=doctor_id, patient_id=patient_id, appointment_date=appointment_date)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@router.put("/appointments/{appointment_id}", response_model=schemas.AppointmentResponse)
def update_appointment(doctor_id: int, patient_id: int, appointment_id: int, appointment_update: schemas.Appointment, db: Session = Depends(get_db)):
    doctor_exists = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor_exists:
        raise HTTPException(status_code=404, detail="Doctor not found")

    patient_exists = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient_exists:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    for key, value in appointment_update.model_dump(exclude_unset=True).items():
        setattr(db_appointment, key, value)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@router.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(db_appointment)
    db.commit()
    return {"message": "Appointment deleted successfully"}

