# api/services/stats_service.py
from api.config.db import get_connection


def get_statistics():
    """
    Obtiene las estadísticas del sistema desde la vista_estadisticas
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM vista_estadisticas")
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            # Convertir Decimal a float para JSON
            estadisticas = {
                "total_traducciones": result["total_traducciones"] or 0,
                "total_contribuciones": result["total_contribuciones"] or 0,
                "contribuciones_pendientes": result["contribuciones_pendientes"] or 0,
                "contribuciones_aprobadas": result["contribuciones_aprobadas"] or 0,
                "senas_oficiales": result["senas_oficiales"] or 0,
                "reportes_activos": result["reportes_activos"] or 0,
                "precision_modelo": float(result["precision_modelo"]) if result["precision_modelo"] else 0.0,
                "fecha_actualizacion": result["fecha_actualizacion"].isoformat() if result["fecha_actualizacion"] else None
            }
            return estadisticas, None
        else:
            # Return default values if no data
            return {
                "total_traducciones": 0,
                "total_contribuciones": 0,
                "contribuciones_pendientes": 0,
                "contribuciones_aprobadas": 0,
                "senas_oficiales": 0,
                "reportes_activos": 0,
                "precision_modelo": 0.0,
                "fecha_actualizacion": None
            }, None
            
    except Exception as e:
        return None, str(e)