from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from deps import get_db
from models import NewsletterSubscriber
from schemas import NewsletterSubscriberCreate, NewsletterSubscriberOut

router = APIRouter(prefix="/newsletter", tags=["newsletter"])


@router.post("/", response_model=NewsletterSubscriberOut)
def subscribe_newsletter(payload: NewsletterSubscriberCreate, db: Session = Depends(get_db)):

    exists = db.query(NewsletterSubscriber).filter(
        NewsletterSubscriber.email == payload.email
    ).first()

    # Case 1: Already active
    if exists and exists.is_active:
        raise HTTPException(status_code=400, detail="Email already subscribed.")

    # Case 2: Exists but inactive → Reactivate
    if exists and not exists.is_active:
        exists.is_active = True
        db.commit()
        db.refresh(exists)
        return exists

    # Case 3: New subscription
    sub = NewsletterSubscriber(email=payload.email)
    db.add(sub)
    db.commit()
    db.refresh(sub)

    return sub

@router.get("/", response_model=list[NewsletterSubscriberOut])
def list_subscribers(db: Session = Depends(get_db)):
    return db.query(NewsletterSubscriber).filter(NewsletterSubscriber.is_active == True).all()

@router.get("/unsubscribe/{token}")
def unsubscribe_newsletter(token: str, db: Session = Depends(get_db)):

    sub = db.query(NewsletterSubscriber).filter(
        NewsletterSubscriber.unsubscribe_token == token,
        NewsletterSubscriber.is_active == True
    ).first()

    if not sub:
        raise HTTPException(status_code=404, detail="Invalid or expired unsubscribe link.")
    
    sub.is_active = False
    db.commit()

    return {"message": "You have been unsubscribed from the newsletter."}