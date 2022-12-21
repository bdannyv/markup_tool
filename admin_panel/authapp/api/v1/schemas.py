from pydantic import BaseModel, EmailStr


class SignInBodyModel(BaseModel):
    user_id: int
    username: str
    password: str


class SignUpBodyModel(SignInBodyModel):
    email: EmailStr
