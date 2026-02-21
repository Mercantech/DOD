from datetime import date

from pydantic import BaseModel


class WeatherForecast(BaseModel):
    date: date
    temperature_c: float
    summary: str | None = None

