from fastapi import FastAPI
from src.routers import doctors, patients, appointments
from src.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(doctors.router, prefix="/api", tags=["Doctors"])
app.include_router(patients.router, prefix="/api", tags=["Patients"])
app.include_router(appointments.router, prefix="/api", tags=["Appointments"])



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)




