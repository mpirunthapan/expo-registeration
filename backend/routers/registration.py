from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from deps import get_db
from models import Registration
from schemas import RegistrationCreate, RegistrationOut

router = APIRouter(prefix="/registrations", tags=["registrations"])


@router.post("/", response_model=RegistrationOut)
def create_registration(payload: RegistrationCreate, db: Session = Depends(get_db)):

    existing = db.query(Registration).filter(
        (Registration.email == payload.email) | 
        (Registration.phone_number == payload.phone_number)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email or phone number already registered.")
    
    reg = Registration(**payload.dict())
    db.add(reg)
    db.commit()
    db.refresh(reg)

    return reg

@router.get("/{registration_id}", response_model=RegistrationOut)
def get_registration(registration_id: int, db: Session = Depends(get_db)):
    reg = db.query(Registration).filter(
        Registration.id == registration_id
    ).first()

    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found.")

    return reg

@router.get("/", response_model=list[RegistrationOut])
def list_registrations(db: Session = Depends(get_db)):
    regs = db.query(Registration).all()
    return regs