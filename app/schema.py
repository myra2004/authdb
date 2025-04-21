from pydantic import BaseModel

class AuthRegistration(BaseModel):
    username: str
    password: str

class AuthRegistrationResponse(AuthRegistration):
    id: int
    role: str

class AuthLogin(BaseModel):
    username: str
    password: str

class AuthLoginResponse(AuthLogin):
    id: int
    role: str