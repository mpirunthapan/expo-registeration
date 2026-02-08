from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from deps import get_db
from models import AdminUser
from schemas import AdminUserLogin, AdminUserCreate, AdminUserOut, AdminPasswordUpdate
from security import verify_password, hash_password

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/create", response_model=dict)
def create_admin_user(payload: AdminUserLogin, db: Session = Depends(get_db)):
    existing = db.query(AdminUser).filter(
        AdminUser.email == payload.email
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Admin user already exists.")

    admin_user = AdminUser(
        email=payload.email,
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
        AdminUser.email == payload.email
    ).first()

    if not admin or not verify_password(payload.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    if not admin.is_active:
        raise HTTPException(status_code=403, detail="Admin user is inactive.")

    return {"message": "Login successful"}

@router.post("/deactivate/{admin_id}")
def deactivate_admin(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(AdminUser).filter(
        AdminUser.id == admin_id
    ).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin user not found.")

    admin.is_active = False
    db.commit()

    return {"message": "Admin user deactivated successfully"}

@router.put("/update-password/{admin_id}")
def update_admin_password(admin_id: int, payload: AdminPasswordUpdate, db: Session = Depends(get_db)):
    admin = db.query(AdminUser).filter(
        AdminUser.id == admin_id
    ).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin user not found.")

    admin.password_hash = hash_password(payload.new_password)
    db.commit()

    return {"message": "Admin password updated successfully"}