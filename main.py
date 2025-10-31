from fastapi import FastAPI
from database import Base, engine
from routers import user_router, education_router, admin_router

app = FastAPI(title="Job Portal API")

Base.metadata.create_all(bind=engine)

app.include_router(user_router.router)

app.include_router(education_router.router)
app.include_router(admin_router.router)
