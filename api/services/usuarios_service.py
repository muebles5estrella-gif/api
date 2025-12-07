"""Usuarios Service - Database operations for user management"""

from api.config.db import get_connection
import bcrypt
import traceback

def get_all_usuarios():
    """Get all users with their details"""
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    u.id_usuario,
                    u.nombre_completo,
                    u.correo,
                    u.tipo_documento,
                    u.numero_documento,
                    u.id_rol,
                    u.estado,
                    u.fecha_registro
                FROM usuarios u
                ORDER BY u.fecha_registro DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            
            if not rows:
                return [], None
            
            usuarios = []
            for row in rows:
                usuarios.append({
                    "id_usuario": row["id_usuario"],
                    "nombre_completo": row["nombre_completo"],
                    "correo": row["correo"],
                    "tipo_documento": row["tipo_documento"],
                    "numero_documento": row["numero_documento"],
                    "id_rol": row["id_rol"],
                    "estado": row["estado"],
                    "fecha_registro": row["fecha_registro"].isoformat() if row["fecha_registro"] else None
                })
            
            return usuarios, None
            
    except Exception as e:
        print(f"Error en get_all_usuarios: {str(e)}")
        traceback.print_exc()
        return None, str(e)
    finally:
        if connection:
            connection.close()


def create_usuario(nombre_completo, correo, contrasena, tipo_documento, numero_documento, id_rol, id_creador, estado="activo"):
    """Create a new user"""
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            # Check if email already exists
            cursor.execute("SELECT id_usuario FROM usuarios WHERE correo = %s", (correo,))
            if cursor.fetchone():
                return None, "El correo electrónico ya está registrado"
            
            # Check if document already exists
            cursor.execute("SELECT id_usuario FROM usuarios WHERE numero_documento = %s", (numero_documento,))
            if cursor.fetchone():
                return None, "El número de documento ya está registrado"
            
            # Hash password
            hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            query = """
                INSERT INTO usuarios 
                (nombre_completo, correo, contrasena, tipo_documento, numero_documento, id_rol, id_creador, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                nombre_completo,
                correo,
                hashed_password,
                tipo_documento,
                numero_documento,
                id_rol,
                id_creador,
                estado
            ))
            connection.commit()
            
            return cursor.lastrowid, None
            
    except Exception as e:
        print(f"Error en create_usuario: {str(e)}")
        traceback.print_exc()
        if connection:
            connection.rollback()
        return None, str(e)
    finally:
        if connection:
            connection.close()


def update_usuario(id_usuario, nombre_completo=None, correo=None, contrasena=None, 
                   tipo_documento=None, numero_documento=None, id_rol=None, estado=None):
    """Update an existing user"""
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            # Check if user exists
            cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            if not cursor.fetchone():
                return False, "Usuario no encontrado"
            
            # Build dynamic update query
            updates = []
            params = []
            
            if nombre_completo is not None:
                updates.append("nombre_completo = %s")
                params.append(nombre_completo)
            
            if correo is not None:
                # Check if email is already used by another user
                cursor.execute("SELECT id_usuario FROM usuarios WHERE correo = %s AND id_usuario != %s", (correo, id_usuario))
                if cursor.fetchone():
                    return False, "El correo electrónico ya está en uso"
                updates.append("correo = %s")
                params.append(correo)
            
            if contrasena is not None and contrasena.strip():
                hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                updates.append("contrasena = %s")
                params.append(hashed_password)
            
            if tipo_documento is not None:
                updates.append("tipo_documento = %s")
                params.append(tipo_documento)
            
            if numero_documento is not None:
                # Check if document is already used by another user
                cursor.execute("SELECT id_usuario FROM usuarios WHERE numero_documento = %s AND id_usuario != %s", 
                             (numero_documento, id_usuario))
                if cursor.fetchone():
                    return False, "El número de documento ya está en uso"
                updates.append("numero_documento = %s")
                params.append(numero_documento)
            
            if id_rol is not None:
                updates.append("id_rol = %s")
                params.append(id_rol)
            
            if estado is not None:
                updates.append("estado = %s")
                params.append(estado)
            
            if not updates:
                return True, None
            
            params.append(id_usuario)
            query = f"UPDATE usuarios SET {', '.join(updates)} WHERE id_usuario = %s"
            
            cursor.execute(query, params)
            connection.commit()
            
            return True, None
            
    except Exception as e:
        print(f"Error en update_usuario: {str(e)}")
        traceback.print_exc()
        if connection:
            connection.rollback()
        return False, str(e)
    finally:
        if connection:
            connection.close()


def delete_usuario(id_usuario):
    """Delete a user (or mark as inactive)"""
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            # Check if user exists
            cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            if not cursor.fetchone():
                return False, "Usuario no encontrado"
            
            # Instead of deleting, mark as inactive to preserve referential integrity
            query = "UPDATE usuarios SET estado = 'inactivo' WHERE id_usuario = %s"
            cursor.execute(query, (id_usuario,))
            connection.commit()
            
            return True, None
            
    except Exception as e:
        print(f"Error en delete_usuario: {str(e)}")
        traceback.print_exc()
        if connection:
            connection.rollback()
        return False, str(e)
    finally:
        if connection:
            connection.close()
