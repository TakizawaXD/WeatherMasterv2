from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func
from src.core.database import Base
from datetime import datetime

class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), index=True, nullable=False)
    country = Column(String(10), nullable=True)
    temperature = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    temperature_min = Column(Float, nullable=False)
    temperature_max = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    visibility = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    wind_deg = Column(Float, nullable=True)
    cloudiness = Column(Float, nullable=True)
    condition = Column(String(50), nullable=False)
    description = Column(String(200), nullable=False)
    sunrise = Column(DateTime, nullable=True)
    sunset = Column(DateTime, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    is_forecast = Column(Boolean, default=False, nullable=False)
    forecast_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<WeatherData(city='{self.city}', temperature={self.temperature}, timestamp='{self.timestamp}')>"