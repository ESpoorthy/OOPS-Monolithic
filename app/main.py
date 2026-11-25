"""Single FastAPI application composed from internal feature routers."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import APP_TITLE, APP_DESCRIPTION, APP_VERSION, ALLOWED_ORIGINS
from app.routes import (
    health_routes, crop_routes, field_routes, disease_routes,
    market_routes, calendar_routes, advisory_routes,
)

app = FastAPI(title=APP_TITLE, description=APP_DESCRIPTION, version=APP_VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for module in (
    health_routes, crop_routes, field_routes, disease_routes,
    market_routes, calendar_routes, advisory_routes,
):
    app.include_router(module.router)


@app.get("/", include_in_schema=False)
def root():
    return {"name": APP_TITLE, "status": "ready", "version": APP_VERSION}
