from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException, status

class UserLoginSchema(BaseModel):
    user_name: str = Field(..., min_length=3, max_length=150, description="The username of the user")
    password: str = Field(..., min_length=6, max_length=100, description="The password of the user")

class UserRegisterSchema(BaseModel):
    user_name: str = Field(..., min_length=3, max_length=150, description="The username of the user")
    password: str = Field(..., min_length=6, max_length=100, description="The password of the user")
    password_confirm: str = Field(..., min_length=6, max_length=100, description="The password confirmation of the user")

    @field_validator("password_confirm")
    def passwords_match(cls, password_confirm, validation):
        if (password_confirm != validation.data.get("password")):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
        return password_confirm