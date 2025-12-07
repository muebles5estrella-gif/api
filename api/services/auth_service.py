# api/services/auth_service.py
from api.models.auth_model import get_user_by_email
from api.utils.security_utils import verify_password, create_access_token


def login_user(correo: str, contrasena: str):
    user = get_user_by_email(correo)

    if not user:
        return None, "Usuario no encontrado"

    if not verify_password(contrasena, user["contrasena"]):
        return None, "Contraseña incorrecta"

    if user["estado"] != "activo":
        return None, "Usuario inactivo"

    token = create_access_token({
        "user_id": user["id_usuario"],
        "role": user["id_rol"],
        "email": user["correo"],
    })

    return {
        "id": user["id_usuario"],
        "nombre": user["nombre_completo"],
        "rol": user["id_rol"],
        "token": token,
    }, None
