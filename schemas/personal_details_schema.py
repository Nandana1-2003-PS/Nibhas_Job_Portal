from pydantic import BaseModel

class PersonalDetailsBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    date_of_birth: str
    address: str
    city: str
    state: str
    pincode: str

class PersonalDetailsCreate(PersonalDetailsBase):
    pass

class PersonalDetailsUpdate(PersonalDetailsBase):
    pass

class PersonalDetailsResponse(PersonalDetailsBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True