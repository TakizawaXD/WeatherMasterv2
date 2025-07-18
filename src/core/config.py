# src/core/config.py

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # OpenWeatherMap API Configuration
    OPENWEATHER_API_KEY: str # Pydantic-settings buscará esto en el .env
    OPENWEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5"

    # Database Configuration
    DATABASE_URL: str # Pydantic-settings buscará esto en el .env

    # Cache Configuration
    CACHE_EXPIRY_MINUTES: int = 15

    # API Configuration
    API_TITLE: str = "WeatherMaster API"
    API_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"  # Esto le dice a Pydantic-settings que cargue variables desde .env
        case_sensitive = True

settings = Settings()