# api/controllers/contribuciones_routes.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from api.services.contribuciones_service import (
    get_all_contribuciones, 
    aprobar_contribucion, 
    rechazar_contribucion
)

router = APIRouter()


class AprobarContribucion(BaseModel):
    observaciones: Optional[str] = None
    id_usuario_envio: int


@router.get("")
def obtener_contribuciones():
    """
    Obtiene todas las contribuciones de señas
    """
    contribuciones, error = get_all_contribuciones()

    if error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error
        )

    return {
        "success": True,
        "data": contribuciones
    }


@router.put("/{id_contribucion}/aprobar")
def aprobar_contribucion_endpoint(id_contribucion: int, data: AprobarContribucion):
    """
    Aprueba una contribución y la agrega al repositorio oficial
    """
    success, error = aprobar_contribucion(
        id_contribucion, 
        data.id_usuario_envio, 
        data.observaciones
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error
        )

    return {
        "success": True,
        "message": "Contribución aprobada y agregada al repositorio oficial"
    }


@router.delete("/{id_contribucion}")
def rechazar_contribucion_endpoint(id_contribucion: int):
    """
    Rechaza y elimina una contribución
    """
    success, error = rechazar_contribucion(id_contribucion)

    if error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error
        )

    return {
        "success": True,
        "message": "Contribución rechazada"
    }
