from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from app.db import create_db_and_tables, get_db
from app.models import Farmer, FarmerCreate, FarmerRead, Provincia


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # corre uma vez no arranque
    yield


app = FastAPI(title="API de Agricultores", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/farmers", response_model=FarmerRead, status_code=201)
def create_farmer(farmer: FarmerCreate, db: Session = Depends(get_db)):
    db_farmer = Farmer.model_validate(farmer)
    db.add(db_farmer)
    db.commit()
    db.refresh(db_farmer)
    return db_farmer


@app.get("/farmers", response_model=list[FarmerRead])
def list_farmers(
    provincia: Provincia | None = None,
    db: Session = Depends(get_db),
):
    statement = select(Farmer)
    if provincia is not None:
        statement = statement.where(Farmer.provincia == provincia)
    return db.exec(statement).all()


@app.get("/farmers/{farmer_id}", response_model=FarmerRead)
def get_farmer(farmer_id: int, db: Session = Depends(get_db)):
    farmer = db.get(Farmer, farmer_id)
    if farmer is None:
        raise HTTPException(status_code=404, detail="Agricultor não encontrado")
    return farmer