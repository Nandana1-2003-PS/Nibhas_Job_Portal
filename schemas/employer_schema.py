from pydantic import BaseModel

class EmployerCreate(BaseModel):
    company_name: str
    username: str
    email: str
    password: str

class EmployerLogin(BaseModel):
    username: str
    password: str

class EmployerUpdate(BaseModel):
    company_name: str | None = None
    email: str | None = None

class EmployerResponse(BaseModel):
    id: int
    company_name: str
    username: str
    email: str

    class Config:
        from_attributes = True
