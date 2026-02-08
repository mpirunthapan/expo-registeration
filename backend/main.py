from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers.registration import router as registration_router
from routers.admin import router as admin_router
from routers.newsletter import router as newsletter_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expo Registration API",
    description="API for managing expo registrations, admin logins, and newsletter subscriptions.",
    version="1.0.0"
)

# POST Registration endpoint
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Expo Registration Backend Running 🚀"}

app.include_router(registration_router)
app.include_router(admin_router)
app.include_router(newsletter_router)