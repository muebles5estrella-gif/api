# api/services/contribuciones_service.py
from api.config.db import get_connection
from datetime import datetime


def get_all_contribuciones():
    """
    Obtiene todas las contribuciones de señas
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                id_contribucion,
                palabra_asociada,
                descripcion,
                archivo_video,
                estado,
                fecha_contribucion,
                fecha_gestion,
                fecha_repositorio,
                observaciones_gestion
            FROM contribuciones_senas
            ORDER BY 
                CASE estado 
                    WHEN 'pendiente' THEN 1
                    WHEN 'aprobada' THEN 2
                END,
                fecha_contribucion DESC
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if not rows:
            return [], None
        
        contribuciones = []
        for row in rows:
            contribuciones.append({
                "id_contribucion": row["id_contribucion"],
                "palabra_asociada": row["palabra_asociada"],
                "descripcion": row["descripcion"],
                "archivo_video": row["archivo_video"],
                "id_usuario_envio": None,  # Campo no disponible en la tabla actual
                "estado": row["estado"],
                "fecha_contribucion": row["fecha_contribucion"].isoformat() if row["fecha_contribucion"] else None,
                "fecha_gestion": row["fecha_gestion"].isoformat() if row["fecha_gestion"] else None,
                "fecha_repositorio": row["fecha_repositorio"].isoformat() if row["fecha_repositorio"] else None,
                "observaciones_gestion": row["observaciones_gestion"]
            })
        
        return contribuciones, None
            
    except Exception as e:
        print(f"Error en get_all_contribuciones: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, str(e)


def aprobar_contribucion(id_contribucion, id_usuario_envio, observaciones=None):
    """
    Aprueba una contribución y la agrega al repositorio oficial
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # 1. Get contribution data
        cursor.execute("""
            SELECT palabra_asociada, archivo_video, descripcion
            FROM contribuciones_senas
            WHERE id_contribucion = %s
        """, (id_contribucion,))
        
        contrib = cursor.fetchone()
        
        if not contrib:
            cursor.close()
            conn.close()
            return False, "Contribución no encontrada"
        
        # 2. Update contribution status
        cursor.execute("""
            UPDATE contribuciones_senas
            SET estado = 'aprobada',
                fecha_gestion = %s,
                fecha_repositorio = %s,
                observaciones_gestion = %s,
                id_usuario_envio = %s
            WHERE id_contribucion = %s
        """, (datetime.now(), datetime.now(), observaciones, id_usuario_envio, id_contribucion))
        
        # 3. Insert into official repository
        cursor.execute("""
            INSERT INTO repositorio_senas_oficial 
            (palabra_asociada, archivo_video, id_contribucion_origen, id_usuario_valido, fecha_validacion)
            VALUES (%s, %s, %s, %s, %s)
        """, (contrib["palabra_asociada"], contrib["archivo_video"], id_contribucion, id_usuario_envio, datetime.now()))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, None
            
    except Exception as e:
        return False, str(e)


def rechazar_contribucion(id_contribucion):
    """
    Rechaza y elimina una contribución
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM contribuciones_senas
            WHERE id_contribucion = %s
        """, (id_contribucion,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, None
            
    except Exception as e:
        return False, str(e)
