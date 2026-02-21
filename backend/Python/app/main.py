from fastapi import FastAPI

from app.api.routes.weather import router as weather_router


def create_app() -> FastAPI:
    app = FastAPI(title="Demo API")
    app.include_router(weather_router)

    @app.get("/healthz")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()

