from pydantic import BaseModel, EmailStr


class SignInBodyModel(BaseModel):
    username: str
    password: str


class SignUpBodyModel(SignInBodyModel):
    email: EmailStr
