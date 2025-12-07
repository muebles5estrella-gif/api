from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.controllers.auth_routes import router as auth_router
from api.controllers.stats_routes import router as stats_router
from api.controllers.reportes_routes import router as reportes_router
from api.controllers.contribuciones_routes import router as contribuciones_router
from api.controllers.usuarios_routes import router as usuarios_router

app = FastAPI(title="Sign Technology API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar el dominio exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(auth_router, prefix="/api/auth")
app.include_router(stats_router, prefix="/api/stats")
app.include_router(reportes_router, prefix="/api/reportes")
app.include_router(contribuciones_router, prefix="/api/contribuciones")
app.include_router(usuarios_router, prefix="/api/usuarios")

# Health 
@app.get("/")
def health_root():
    return {"status": "ok", "message": "API is running", "version": "1.0.0",}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.run:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
