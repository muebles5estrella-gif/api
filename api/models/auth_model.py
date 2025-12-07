# api/models/auth_model.py
from api.config.db import get_connection


def get_user_by_email(correo: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id_usuario, nombre_completo, correo, contrasena, id_rol, estado
        FROM usuarios
        WHERE correo = %s
        LIMIT 1
        """,
        (correo,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()
    return user
