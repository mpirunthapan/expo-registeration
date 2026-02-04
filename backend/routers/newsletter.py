from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from deps import get_db
from models import NewsletterSubscriber
from schemas import NewsletterSubscriberCreate, NewsletterSubscriberOut

router = APIRouter(prefix="/newsletter", tags=["newsletter"])


@router.post("/", response_model=NewsletterSubscriberOut)
def subscribe_newsletter(payload: NewsletterSubscriberCreate, db: Session = Depends(get_db)):

    exists = db.query(NewsletterSubscriber).filter(
        NewsletterSubscriber.email == payload.email
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Email already subscribed to the newsletter.")
    
    sub = NewsletterSubscriber(**payload.dict())
    db.add(sub)
    db.commit()
    db.refresh(sub)

    return sub

@router.get("/", response_model=list[NewsletterSubscriberOut])
def list_subscribers(db: Session = Depends(get_db)):
    subs = db.query(NewsletterSubscriber).all()
    return subs