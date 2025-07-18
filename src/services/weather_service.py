import requests
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import List, Optional
from src.core.config import settings
from src.models.weather import WeatherData

class WeatherService:
    def __init__(self, db: Session):
        self.db = db
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = settings.OPENWEATHER_BASE_URL
        self.cache_expiry_minutes = settings.CACHE_EXPIRY_MINUTES

    def get_current_weather(self, city: str) -> dict:
        """Get current weather with intelligent caching"""
        
        # Check cache first
        cached_weather = self._get_cached_weather(city)
        if cached_weather:
            return self._format_weather_response(cached_weather)
        
        # Fetch from API
        weather_data = self._fetch_current_weather_from_api(city)
        
        # Cache the result
        self._cache_weather_data(weather_data, city)
        
        return weather_data

    def get_forecast(self, city: str) -> List[dict]:
        """Get 5-day forecast with intelligent caching"""
        
        # Check cache first
        cached_forecast = self._get_cached_forecast(city)
        if cached_forecast:
            return [self._format_forecast_response(item) for item in cached_forecast]
        
        # Fetch from API
        forecast_data = self._fetch_forecast_from_api(city)
        
        # Cache the result
        self._cache_forecast_data(forecast_data, city)
        
        return forecast_data

    def _get_cached_weather(self, city: str) -> Optional[WeatherData]:
        """Get cached weather data if not expired"""
        cache_threshold = datetime.now() - timedelta(minutes=self.cache_expiry_minutes)
        
        return self.db.query(WeatherData).filter(
            and_(
                WeatherData.city.ilike(f"%{city}%"),
                WeatherData.is_forecast == False,
                WeatherData.timestamp >= cache_threshold
            )
        ).order_by(desc(WeatherData.timestamp)).first()

    def _get_cached_forecast(self, city: str) -> List[WeatherData]:
        """Get cached forecast data if not expired"""
        cache_threshold = datetime.now() - timedelta(minutes=self.cache_expiry_minutes)
        
        return self.db.query(WeatherData).filter(
            and_(
                WeatherData.city.ilike(f"%{city}%"),
                WeatherData.is_forecast == True,
                WeatherData.timestamp >= cache_threshold
            )
        ).order_by(WeatherData.forecast_date).all()

    def _fetch_current_weather_from_api(self, city: str) -> dict:
        """Fetch current weather from OpenWeatherMap API"""
        url = f"{self.base_url}/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "temperature_min": data["main"]["temp_min"],
                "temperature_max": data["main"]["temp_max"],
                "pressure": data["main"]["pressure"],
                "humidity": data["main"]["humidity"],
                "visibility": data.get("visibility", 0),
                "wind_speed": data.get("wind", {}).get("speed", 0),
                "wind_deg": data.get("wind", {}).get("deg", 0),
                "cloudiness": data.get("clouds", {}).get("all", 0),
                "condition": data["weather"][0]["main"],
                "description": data["weather"][0]["description"],
                "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]),
                "sunset": datetime.fromtimestamp(data["sys"]["sunset"]),
                "timestamp": datetime.now()
            }
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch weather data: {str(e)}")
        except KeyError as e:
            raise Exception(f"Invalid response format: {str(e)}")

    def _fetch_forecast_from_api(self, city: str) -> List[dict]:
        """Fetch 5-day forecast from OpenWeatherMap API"""
        url = f"{self.base_url}/forecast"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Group forecast by date
            daily_forecasts = {}
            
            for item in data["list"]:
                date = datetime.fromtimestamp(item["dt"]).date()
                date_str = date.strftime("%Y-%m-%d")
                
                if date_str not in daily_forecasts:
                    daily_forecasts[date_str] = {
                        "date": date,
                        "temps": [],
                        "conditions": [],
                        "descriptions": []
                    }
                
                daily_forecasts[date_str]["temps"].append(item["main"]["temp"])
                daily_forecasts[date_str]["conditions"].append(item["weather"][0]["main"])
                daily_forecasts[date_str]["descriptions"].append(item["weather"][0]["description"])
            
            # Convert to list format
            forecast_list = []
            for date_str, day_data in list(daily_forecasts.items())[:5]:  # 5 days
                forecast_list.append({
                    "date": day_data["date"],
                    "temperature_min": min(day_data["temps"]),
                    "temperature_max": max(day_data["temps"]),
                    "condition": max(set(day_data["conditions"]), key=day_data["conditions"].count),
                    "description": max(set(day_data["descriptions"]), key=day_data["descriptions"].count)
                })
            
            return forecast_list
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch forecast data: {str(e)}")
        except KeyError as e:
            raise Exception(f"Invalid response format: {str(e)}")

    def _cache_weather_data(self, weather_data: dict, city: str):
        """Cache weather data to database"""
        try:
            weather_record = WeatherData(
                city=weather_data["city"],
                country=weather_data["country"],
                temperature=weather_data["temperature"],
                feels_like=weather_data["feels_like"],
                temperature_min=weather_data["temperature_min"],
                temperature_max=weather_data["temperature_max"],
                pressure=weather_data["pressure"],
                humidity=weather_data["humidity"],
                visibility=weather_data["visibility"],
                wind_speed=weather_data["wind_speed"],
                wind_deg=weather_data["wind_deg"],
                cloudiness=weather_data["cloudiness"],
                condition=weather_data["condition"],
                description=weather_data["description"],
                sunrise=weather_data["sunrise"],
                sunset=weather_data["sunset"],
                timestamp=weather_data["timestamp"],
                is_forecast=False
            )
            
            self.db.add(weather_record)
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            print(f"Error caching weather data: {str(e)}")

    def _cache_forecast_data(self, forecast_data: List[dict], city: str):
        """Cache forecast data to database"""
        try:
            for day_forecast in forecast_data:
                forecast_record = WeatherData(
                    city=city,
                    country="",
                    temperature=(day_forecast["temperature_min"] + day_forecast["temperature_max"]) / 2,
                    feels_like=(day_forecast["temperature_min"] + day_forecast["temperature_max"]) / 2,
                    temperature_min=day_forecast["temperature_min"],
                    temperature_max=day_forecast["temperature_max"],
                    pressure=0,
                    humidity=0,
                    visibility=0,
                    wind_speed=0,
                    wind_deg=0,
                    cloudiness=0,
                    condition=day_forecast["condition"],
                    description=day_forecast["description"],
                    timestamp=datetime.now(),
                    is_forecast=True,
                    forecast_date=day_forecast["date"]
                )
                
                self.db.add(forecast_record)
            
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            print(f"Error caching forecast data: {str(e)}")

    def _format_weather_response(self, weather: WeatherData) -> dict:
        """Format weather data for API response"""
        return {
            "city": weather.city,
            "country": weather.country,
            "temperature": weather.temperature,
            "feels_like": weather.feels_like,
            "temperature_min": weather.temperature_min,
            "temperature_max": weather.temperature_max,
            "pressure": weather.pressure,
            "humidity": weather.humidity,
            "visibility": weather.visibility,
            "wind_speed": weather.wind_speed,
            "wind_deg": weather.wind_deg,
            "cloudiness": weather.cloudiness,
            "condition": weather.condition,
            "description": weather.description,
            "sunrise": weather.sunrise,
            "sunset": weather.sunset,
            "timestamp": weather.timestamp
        }

    def _format_forecast_response(self, forecast: WeatherData) -> dict:
        """Format forecast data for API response"""
        return {
            "date": forecast.forecast_date,
            "temperature_min": forecast.temperature_min,
            "temperature_max": forecast.temperature_max,
            "condition": forecast.condition,
            "description": forecast.description
        }