from pydantic import BaseModel, Field, EmailStr, validator
import re



class SUuserRegister(BaseModel):
    email: EmailStr = Field(..., description="email")
    password: str = Field(..., min_length=5, max_length=50, description="Password from 5 to 50 signs")
    phone_number: str = Field(..., description="Phone number in the international format, starting with '+'")
    first_name: str = Field(..., min_length=3, max_length=50, description="firstname, from 3 to 50 symbols")
    last_name: str = Field(..., min_length=3, max_length=50, description="last name, from 3 to 50 signs")


    @validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str):
        if not re.match(r"^\+\d{5,15}$", value):
              raise ValueError('The phone number must  with "+" and contain from 5 to 15 numbers')
        return value


class SUserAuth(BaseModel):
    email: EmailStr = Field(description="email address", )
    password: str = Field(description="password", min_length=8, max_length=16)