# api/controllers/stats_routes.py
from fastapi import APIRouter, HTTPException, status
from api.services.stats_service import get_statistics

router = APIRouter()


@router.get("/estadisticas")
def obtener_estadisticas():
    """
    Obtiene las estadísticas generales del sistema desde la vista_estadisticas
    """
    estadisticas, error = get_statistics()

    if error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error
        )

    return {
        "success": True,
        "data": estadisticas
    }
