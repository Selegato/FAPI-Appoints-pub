from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from src import schemas, models

router = APIRouter()



@router.get("/doctors/", response_model=List[schemas.DoctorResponse])
def get_doctors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    doctors = db.query(models.Doctor).offset(skip).limit(limit).all()
    if not doctors:
        raise HTTPException(status_code=404, detail="No doctors found")
    return doctors

@router.get("/doctors/{doctor_id}", response_model=schemas.DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_doctor

@router.post("/doctors/")
def add_doctor(doctor: schemas.Doctor, db: Session = Depends(get_db)):
    db_doctor = models.Doctor(**doctor.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@router.put("/doctors/{doctor_id}", response_model=schemas.DoctorResponse)
def update_doctor(doctor_id: int, doctor_update: schemas.Doctor, db: Session = Depends(get_db)):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    for key, value in doctor_update.model_dump(exclude_unset=True).items():
        setattr(db_doctor, key, value)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@router.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.delete(db_doctor)
    db.commit()
    return {"message": "Doctor deleted successfully"}