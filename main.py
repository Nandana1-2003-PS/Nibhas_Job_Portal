from fastapi import FastAPI
from database import Base, engine
from routers import user_router, education_router, admin_router ,personal_details_router
from routers import preferred_router
from routers import employer_router,skill_router 


app = FastAPI(title="Job Portal API")

Base.metadata.create_all(bind=engine)

app.include_router(user_router.router)

app.include_router(personal_details_router.router)

app.include_router(education_router.router)
app.include_router(admin_router.router)
app.include_router(preferred_router.router)
app.include_router(employer_router.router)
app.include_router(skill_router.router)