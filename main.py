"""
Punto de entrada principal de la API HotelEvo.
Registra todos los routers y configura la aplicación FastAPI.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.auth_router import router as auth_router
from routers.catalogos_router import router as catalogos_router
from routers.huesped_router import router as huesped_router
from routers.personal_router import router as personal_router
from routers.habitacion_router import router as habitacion_router
from routers.reserva_router import router as reserva_router
from routers.conserjeria_router import router as conserjeria_router
from routers.hospedaje_router import router as hospedaje_router
from routers.documento_router import router as documento_router
from routers.pago_router import router as pago_router
from routers.encuesta_router import router as encuesta_router

app = FastAPI(
    title="HotelEvo API",
    description="API de gestión hotelera: reservas, hospedaje, conserjería, pagos y encuestas.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://proyecto21-front.vercel.app/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Registro de routers ────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(catalogos_router)
app.include_router(huesped_router)
app.include_router(personal_router)
app.include_router(habitacion_router)
app.include_router(reserva_router)
app.include_router(conserjeria_router)
app.include_router(hospedaje_router)
app.include_router(documento_router)
app.include_router(pago_router)
app.include_router(encuesta_router)


@app.get("/", tags=["Root"])
def root():
    return {"mensaje": "HotelEvo API activa. Visita /docs para la documentación."}