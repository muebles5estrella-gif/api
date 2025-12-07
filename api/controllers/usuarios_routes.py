"""Usuarios Routes - API endpoints for user management"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional
from api.services import usuarios_service

router = APIRouter()


class UsuarioCreate(BaseModel):
    nombre_completo: str
    correo: EmailStr
    contrasena: str
    tipo_documento: str
    numero_documento: str
    id_rol: int
    id_creador: int
    estado: str = "activo"


class UsuarioUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    correo: Optional[EmailStr] = None
    contrasena: Optional[str] = None
    tipo_documento: Optional[str] = None
    numero_documento: Optional[str] = None
    id_rol: Optional[int] = None
    estado: Optional[str] = None


@router.get("")
async def obtener_usuarios():
    """Get all users"""
    usuarios, error = usuarios_service.get_all_usuarios()
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios: {error}"
        )
    
    return {
        "success": True,
        "data": usuarios,
        "total": len(usuarios)
    }


@router.post("")
async def crear_usuario(usuario: UsuarioCreate):
    """Create a new user"""
    usuario_id, error = usuarios_service.create_usuario(
        nombre_completo=usuario.nombre_completo,
        correo=usuario.correo,
        contrasena=usuario.contrasena,
        tipo_documento=usuario.tipo_documento,
        numero_documento=usuario.numero_documento,
        id_rol=usuario.id_rol,
        id_creador=usuario.id_creador,
        estado=usuario.estado
    )
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return {
        "success": True,
        "message": "Usuario creado exitosamente",
        "id": usuario_id
    }


@router.put("/{id_usuario}")
async def actualizar_usuario(id_usuario: int, usuario: UsuarioUpdate):
    """Update an existing user"""
    success, error = usuarios_service.update_usuario(
        id_usuario=id_usuario,
        nombre_completo=usuario.nombre_completo,
        correo=usuario.correo,
        contrasena=usuario.contrasena,
        tipo_documento=usuario.tipo_documento,
        numero_documento=usuario.numero_documento,
        id_rol=usuario.id_rol,
        estado=usuario.estado
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error or "Error al actualizar usuario"
        )
    
    return {
        "success": True,
        "message": "Usuario actualizado exitosamente"
    }


@router.delete("/{id_usuario}")
async def eliminar_usuario(id_usuario: int):
    """Delete (mark as inactive) a user"""
    success, error = usuarios_service.delete_usuario(id_usuario)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error or "Error al eliminar usuario"
        )
    
    return {
        "success": True,
        "message": "Usuario eliminado exitosamente"
    }
