from pydantic import BaseModel, EmailStr


class SignInBodyModel(BaseModel):
    user_id: int
    password: str


class SignUpBodyModel(SignInBodyModel):
    username: str
    email: EmailStr
