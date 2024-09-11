from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from src import schemas, models

router = APIRouter()



@router.get("/patients/", response_model=List[schemas.PatientResponse])
def get_patients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    if not patients:
        raise HTTPException(status_code=404, detail="No patients found")
    return patients

@router.get("/patients/{patient_id}", response_model=schemas.PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if db_patient is None:
            raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@router.post("/patients/", response_model=schemas.PatientResponse)
def add_patient(patient: schemas.Patient, db: Session = Depends(get_db)):
    db_patient = models.Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.put("/patients/{patient_id}", response_model=schemas.PatientResponse)
def update_patient(patient_id: int, patient_update: schemas.Patient, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    for key, value in patient_update.model_dump(exclude_unset=True).items():
        setattr(db_patient, key, value)
    return db_patient

@router.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if db_patient is None:     
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(db_patient)
    db.commit()
    return {"message": "Patient deleted successfully"}