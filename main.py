from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
from src.api.weather import weather_router
from src.core.database import engine, Base
from src.core.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🌤️  WeatherMaster API Starting...")
    print(f"📍 OpenWeatherMap API configured: {'✅' if settings.OPENWEATHER_API_KEY else '❌'}")
    yield
    # Shutdown
    print("🌤️  WeatherMaster API Shutting down...")

app = FastAPI(
    title="WeatherMaster API",
    description="Real-time weather information system with intelligent caching",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(weather_router, prefix="/weather", tags=["weather"])

# Serve static files
app.mount("/static", StaticFiles(directory="."), name="static")

# Serve index.html at root
@app.get("/")
async def read_root():
    return FileResponse("index.html")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "WeatherMaster API"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )