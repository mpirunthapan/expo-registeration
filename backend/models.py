from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from database import Base

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    fullname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    work_station = Column(String, nullable=True)
    category = Column(String, nullable=False)
    heard_from = Column(String, nullable=False)
    joined_community = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class NewsletterSubscriber(Base):
    __tablename__ = "newsletter_subscribers"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    unsubscribe_token = Column(String, unique=True, index=True, nullable=True)
    subscribed_at = Column(DateTime(timezone=True), server_default=func.now())