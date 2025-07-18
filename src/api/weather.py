from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.core.database import get_db
from src.services.weather_service import WeatherService

weather_router = APIRouter()

@weather_router.get("/current/{city_name}")
async def get_current_weather(city_name: str, db: Session = Depends(get_db)):
    """Get current weather for a specific city"""
    try:
        weather_service = WeatherService(db)
        weather_data = weather_service.get_current_weather(city_name)
        return weather_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@weather_router.get("/forecast/{city_name}")
async def get_weather_forecast(city_name: str, db: Session = Depends(get_db)):
    """Get 5-day weather forecast for a specific city"""
    try:
        weather_service = WeatherService(db)
        forecast_data = weather_service.get_forecast(city_name)
        return forecast_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@weather_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Weather API"}