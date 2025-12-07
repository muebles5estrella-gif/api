# api/controllers/auth_routes.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from api.services.auth_service import login_user

router = APIRouter()


class LoginDTO(BaseModel):
    correo: EmailStr
    contrasena: str


@router.post("/login")
def login(data: LoginDTO):
    usuario, error = login_user(data.correo, data.contrasena)

    if error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error
        )

    return {
        "message": "Login correcto",
        "usuario": usuario,
    }
