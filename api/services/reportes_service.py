# api/services/reportes_service.py
from api.config.db import get_connection


def get_all_reportes():
    """
    Obtiene todos los reportes de errores ordenados por fecha
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                id_reporte,
                id_traduccion,
                tipo_traduccion,
                descripcion_error,
                evidencia_url,
                prioridad,
                estado,
                fecha_reporte,
                id_usuario_reporta
            FROM reportes_errores
            ORDER BY 
                CASE prioridad
                    WHEN 'alta' THEN 1
                    WHEN 'media' THEN 2
                    WHEN 'baja' THEN 3
                END,
                fecha_reporte DESC
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if not rows:
            return [], None
        
        reportes = []
        for row in rows:
            reportes.append({
                "id_reporte": row["id_reporte"],
                "id_traduccion": row["id_traduccion"],
                "tipo_traduccion": row["tipo_traduccion"],
                "descripcion_error": row["descripcion_error"],
                "evidencia_url": row["evidencia_url"],
                "prioridad": row["prioridad"],
                "estado": row["estado"],
                "fecha_reporte": row["fecha_reporte"].isoformat() if row["fecha_reporte"] else None,
                "id_usuario_reporta": row["id_usuario_reporta"]
            })
        
        return reportes, None
            
    except Exception as e:
        return None, str(e)


def update_reporte_estado(id_reporte, nuevo_estado):
    """
    Actualiza el estado de un reporte
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE reportes_errores
            SET estado = %s
            WHERE id_reporte = %s
        """
        
        cursor.execute(query, (nuevo_estado, id_reporte))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return True, None
            
    except Exception as e:
        return False, str(e)
