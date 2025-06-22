from fastapi import FastAPI
from app.api.routes import router, public_router

app = FastAPI(title="Prueba tecnica backend")

app.include_router(public_router)
app.include_router(router)


