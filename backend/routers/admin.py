from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from deps import get_db
from models import AdminUser
from schemas import AdminUserLogin
from security import verify_password, hash_password

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/create", response_model=dict)
def create_admin_user(payload: AdminUserLogin, db: Session = Depends(get_db)):
    existing = db.query(AdminUser).filter(
        AdminUser.username == payload.username
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Admin user already exists.")

    admin_user = AdminUser(
        username=payload.username,
        password_hash=hash_password(payload.password),
        is_active=True
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    return {"message": "Admin user created successfully"}

@router.post("/login")
def admin_login(payload: AdminUserLogin, db: Session = Depends(get_db)):

    admin = db.query(AdminUser).filter(
        AdminUser.username == payload.username
    ).first()

    if not admin or not verify_password(payload.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    if not admin.is_active:
        raise HTTPException(status_code=403, detail="Admin user is inactive.")

    return {"message": "Login successful"}