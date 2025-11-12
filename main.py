from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import user_router, education_router, admin_router ,personal_details_router
from routers import preferred_router
from routers import employer_router,skill_router 


app = FastAPI(title="Job Portal API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
        "http://192.168.1.34:3000",
        "http://192.168.1.34:5173",
        "http://192.168.1.34:8000",
        "http://192.168.1.34",
    ],  # React dev server ports + local WiFi IP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(user_router.router)

app.include_router(personal_details_router.router)

app.include_router(education_router.router)
app.include_router(admin_router.router)
app.include_router(preferred_router.router)
app.include_router(employer_router.router)
app.include_router(skill_router.router)