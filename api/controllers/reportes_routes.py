# api/controllers/reportes_routes.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from api.services.reportes_service import get_all_reportes, update_reporte_estado

router = APIRouter()


class EstadoUpdate(BaseModel):
    estado: str


@router.get("")
def obtener_reportes():
    """
    Obtiene todos los reportes de errores
    """
    reportes, error = get_all_reportes()

    if error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error
        )

    return {
        "success": True,
        "data": reportes
    }


@router.put("/{id_reporte}/estado")
def actualizar_estado_reporte(id_reporte: int, estado_data: EstadoUpdate):
    """
    Actualiza el estado de un reporte
    """
    success, error = update_reporte_estado(id_reporte, estado_data.estado)

    if error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error
        )

    return {
        "success": True,
        "message": "Estado actualizado correctamente"
    }
