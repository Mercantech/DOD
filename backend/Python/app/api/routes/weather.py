from datetime import date, timedelta
import random

from fastapi import APIRouter

from app.schemas.weather import WeatherForecast

router = APIRouter(prefix="/weather", tags=["weather"])

SUMMARIES = ["Sol", "Skyet", "Regn", "Blæst", "Sne"]


@router.get("/", response_model=list[WeatherForecast])
async def get_forecast(days: int = 5) -> list[WeatherForecast]:
    today = date.today()
    forecasts: list[WeatherForecast] = []
    for i in range(days):
        forecasts.append(
            WeatherForecast(
                date=today + timedelta(days=i),
                temperature_c=random.uniform(-5, 28),
                summary=random.choice(SUMMARIES),
            )
        )
    return forecasts

