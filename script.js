class WeatherApp {
    constructor() {
        this.apiBase = 'http://localhost:8000';
        this.currentCity = '';
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        const searchBtn = document.getElementById('searchBtn');
        const cityInput = document.getElementById('cityInput');

        searchBtn.addEventListener('click', () => this.searchWeather());
        cityInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.searchWeather();
            }
        });

        // Carga la ciudad por defecto al cargar la página
        this.loadDefaultCity();
    }

    async loadDefaultCity() {
        await this.getWeatherData('London');
    }

    async searchWeather() {
        const cityInput = document.getElementById('cityInput');
        const city = cityInput.value.trim();
        
        if (!city) {
            this.showError('Por favor, ingresa un nombre de ciudad.');
            return;
        }

        await this.getWeatherData(city);
    }

    async getWeatherData(city) {
        this.showLoading();
        this.hideError();
        this.hideWeatherDisplay();

        try {
            // Obtener el clima actual
            const currentWeatherResponse = await fetch(`${this.apiBase}/weather/current/${encodeURIComponent(city)}`);
            if (!currentWeatherResponse.ok) {
                const errorData = await currentWeatherResponse.json(); // Intentar leer el detalle del error del backend
                throw new Error(`Error al obtener el clima actual: ${errorData.detail || currentWeatherResponse.statusText}`);
            }
            const currentWeather = await currentWeatherResponse.json();

            // Obtener el pronóstico
            const forecastResponse = await fetch(`${this.apiBase}/weather/forecast/${encodeURIComponent(city)}`);
            if (!forecastResponse.ok) {
                const errorData = await forecastResponse.json(); // Intentar leer el detalle del error del backend
                throw new Error(`Error al obtener el pronóstico: ${errorData.detail || forecastResponse.statusText}`);
            }
            const forecast = await forecastResponse.json();

            this.currentCity = city;
            this.displayWeather(currentWeather, forecast);
            this.hideLoading();
            this.showWeatherDisplay();

        } catch (error) {
            console.error('Error al obtener datos del clima:', error);
            this.hideLoading();
            // Mostrar el mensaje de error directamente del backend si está disponible
            this.showError(error.message || 'No se pudieron obtener los datos del clima. Por favor, verifica el nombre de la ciudad e inténtalo de nuevo.');
        }
    }

    displayWeather(currentWeather, forecast) {
        this.displayCurrentWeather(currentWeather);
        this.displayForecast(forecast);
    }

    displayCurrentWeather(weather) {
        const cityName = document.getElementById('cityName');
        const timestamp = document.getElementById('timestamp');
        const temperature = document.getElementById('temperature');
        const weatherIcon = document.getElementById('weatherIcon');
        const description = document.getElementById('description');
        const feelsLike = document.getElementById('feelsLike');
        const visibility = document.getElementById('visibility');
        const humidity = document.getElementById('humidity');
        const windSpeed = document.getElementById('windSpeed');
        const pressure = document.getElementById('pressure');

        // Asegúrate de que los elementos HTML existan para evitar errores
        if (cityName) cityName.textContent = weather.city;
        if (timestamp && weather.timestamp) timestamp.textContent = new Date(weather.timestamp).toLocaleString();
        if (temperature && weather.temperature !== undefined) temperature.textContent = `${Math.round(weather.temperature)}°C`;
        if (description) description.textContent = weather.description;
        
        // Estos campos ahora deberían venir del backend
        if (feelsLike && weather.feels_like !== undefined) feelsLike.textContent = `Sensación térmica: ${Math.round(weather.feels_like)}°C`;
        // La visibilidad viene en metros del backend, la convertimos a km aquí.
        if (visibility && weather.visibility !== undefined) visibility.textContent = `Visibilidad: ${(weather.visibility / 1000).toFixed(1)} km`; 
        
        if (humidity && weather.humidity !== undefined) humidity.textContent = `Humedad: ${weather.humidity}%`;
        // La velocidad del viento viene en m/s del backend, la convertimos a km/h aquí (1 m/s = 3.6 km/h).
        if (windSpeed && weather.wind_speed !== undefined) windSpeed.textContent = `Viento: ${Math.round(weather.wind_speed * 3.6)} km/h`;
        if (pressure && weather.pressure !== undefined) pressure.textContent = `Presión: ${weather.pressure} hPa`;

        // Establecer el icono del clima usando la nueva propiedad 'condition'
        if (weatherIcon && weather.condition) {
            const iconClass = this.getWeatherIcon(weather.condition);
            weatherIcon.className = `fas ${iconClass}`;
        } else if (weatherIcon) { // Fallback si 'condition' no está presente
            weatherIcon.className = 'fas fa-question-circle'; 
        }
    }

    displayForecast(forecast) {
        const forecastCards = document.getElementById('forecastCards');
        if (!forecastCards) return; // Asegúrate de que el contenedor existe
        forecastCards.innerHTML = '';

        // Filtrar y tomar solo los próximos 5 días si hay más
        const displayableForecast = forecast.slice(0, 5); 

        displayableForecast.forEach(day => {
            const card = document.createElement('div');
            card.className = 'forecast-card';
            
            const date = new Date(day.date); // 'date' ahora viene del backend en formato YYYY-MM-DD
            
            // **** AJUSTE AQUÍ: Usamos 'es-CO' para los días en español de Colombia ****
            const dayName = date.toLocaleDateString('es-CO', { weekday: 'long' }); // Ejemplo: "lunes", "martes"
            const dateStr = date.toLocaleDateString('es-CO', { month: 'short', day: 'numeric' }); // Ejemplo: "jul. 18"
            
            // Si prefieres una versión más corta del día (ej. "lun.", "mar.") puedes usar:
            // const dayName = date.toLocaleDateString('es-CO', { weekday: 'short' }); 
            
            // Asegúrate de que temperature_max y temperature_min existan antes de redondear
            const tempHigh = day.temperature_max !== undefined ? `${Math.round(day.temperature_max)}°` : 'N/A';
            const tempLow = day.temperature_min !== undefined ? `${Math.round(day.temperature_min)}°` : 'N/A';

            card.innerHTML = `
                <div class="forecast-date">${dateStr}</div>
                <div class="forecast-day">${dayName}</div>
                <div class="forecast-icon">
                    <i class="fas ${this.getWeatherIcon(day.condition)}"></i>
                </div>
                <div class="forecast-temps">
                    <span class="forecast-high">${tempHigh}</span>
                    <span class="forecast-low">${tempLow}</span>
                </div>
                <div class="forecast-desc">${day.description}</div>
            `;
            
            forecastCards.appendChild(card);
        });
    }

    // Mapea las condiciones de clima (ej. 'clouds', 'rain') a iconos de Font Awesome
    getWeatherIcon(condition) {
        const iconMap = {
            'clear': 'fa-sun',
            'clouds': 'fa-cloud',
            'rain': 'fa-cloud-rain',
            'drizzle': 'fa-cloud-drizzle',
            'thunderstorm': 'fa-bolt',
            'snow': 'fa-snowflake',
            'mist': 'fa-smog',
            'fog': 'fa-smog',
            'haze': 'fa-smog',
            'smoke': 'fa-smog',
            'dust': 'fa-smog',
            'sand': 'fa-smog',
            'ash': 'fa-smog',
            'squall': 'fa-wind',
            'tornado': 'fa-tornado'
        };
        // Devuelve el icono mapeado o un icono predeterminado si no se encuentra la condición
        return iconMap[condition.toLowerCase()] || 'fa-question-circle'; 
    }

    // Funciones de UI para mostrar/ocultar elementos
    showLoading() {
        const loadingElement = document.getElementById('loading');
        if (loadingElement) loadingElement.classList.remove('hidden');
    }

    hideLoading() {
        const loadingElement = document.getElementById('loading');
        if (loadingElement) loadingElement.classList.add('hidden');
    }

    showError(message) {
        const errorDiv = document.getElementById('error');
        const errorMessage = document.getElementById('errorMessage');
        if (errorDiv) errorDiv.classList.remove('hidden');
        if (errorMessage) errorMessage.textContent = message;
    }

    hideError() {
        const errorDiv = document.getElementById('error');
        if (errorDiv) errorDiv.classList.add('hidden');
    }

    showWeatherDisplay() {
        const weatherDisplayElement = document.getElementById('weatherDisplay');
        if (weatherDisplayElement) weatherDisplayElement.classList.remove('hidden');
    }

    hideWeatherDisplay() {
        const weatherDisplayElement = document.getElementById('weatherDisplay');
        if (weatherDisplayElement) weatherDisplayElement.classList.add('hidden');
    }
}

// Inicializa la aplicación cuando el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', () => {
    new WeatherApp();
});