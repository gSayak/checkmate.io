from pydantic import BaseModel, EmailStr, constr, conint, confloat, validator

class ExpertCreateSchema(BaseModel):
    name: constr(strict=True)
    email: EmailStr
    password: constr(strict=True, min_length=8)
    bio: str = None
    profile_picture_url: str = None

class ServiceCreateSchema(BaseModel):
    service_type: constr(strict=True)
    title: constr(strict=True)
    description: str = None
    price: confloat(strict=True)
    duration: conint(strict=True)

    @validator('service_type')
    def validate_service_type(cls, v):
        if v not in ['video_meeting', 'priority_dm']:
            raise ValueError("Invalid service type. Must be 'video_meeting' or 'priority_dm'.")
        return v

class BookingCreateSchema(BaseModel):
    service_id: constr(strict=True)
    user_email: EmailStr

class MessageCreateSchema(BaseModel):
    booking_id: constr(strict=True)
    message: str