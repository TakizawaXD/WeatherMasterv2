Aquí tienes el `README.md` completo, sin explicaciones de código detalladas y con la imagen del diagrama de estructura que solicitaste.

-----

# WeatherMaster – Sistema de Clima en Tiempo Real

## 📌 Descripción General

**WeatherMaster** es una solución de backend desarrollada con **FastAPI** que proporciona información detallada del clima actual, sensación térmica y pronósticos futuros. Su enfoque está en la eficiencia, escalabilidad y compatibilidad multiplataforma mediante API REST. Utiliza **SQLite** como base de datos relacional para implementar un sistema de caché inteligente, optimizando el rendimiento y reduciendo las llamadas a la API externa. La interfaz de usuario es una aplicación moderna y responsiva construida con **React y TypeScript**, potenciada por **Vite**, que consume estos datos.

-----

## 🎯 Propósito del Proyecto

El propósito de WeatherMaster es ofrecer un sistema de consulta meteorológica eficiente y fácil de usar, con las siguientes funcionalidades clave:

  * **Datos Climáticos en Tiempo Real**: Proporcionar condiciones climáticas actuales para cualquier ciudad del mundo.
  * **Pronóstico de 5 Días**: Ofrecer predicciones meteorológicas detalladas para los próximos cinco días.
  * **Caché Inteligente**: Implementar un sistema de caché de 15 minutos utilizando la base de datos SQLite.
  * **Interfaz de Usuario Moderna**: Disponer de una interfaz de usuario responsiva y atractiva con animaciones meteorológicas dinámicas, construida con React y TypeScript.
  * **API de Alto Rendimiento**: Un backend robusto y rápido desarrollado con FastAPI.
  * **Fácil Configuración**: Asegurar una instalación y configuración sencillas del sistema tanto para el backend como para el frontend.

-----

## 👥 Público Objetivo

  * **Usuarios finales** que buscan una aplicación web intuitiva para consultar el clima desde cualquier dispositivo.
  * **Desarrolladores** interesados en integrar datos meteorológicos en sus propias aplicaciones a través de una API REST robusta.
  * **Empresas** que requieran una base para visualizar o analizar información meteorológica con eficiencia.

-----

## 🛠️ Tecnologías Utilizadas

| Componente          | Tecnología                               | Descripción                                                  |
| :------------------ | :--------------------------------------- | :----------------------------------------------------------- |
| **Backend API** | FastAPI, SQLAlchemy, Uvicorn             | Framework web Python de alto rendimiento, ORM y servidor ASGI. |
| **Base de Datos** | SQLite                                   | Base de datos ligera para el sistema de caché inteligente. |
| **API Externa** | OpenWeatherMap                           | Fuente de datos meteorológicos en tiempo real.             |
| **Comunicación API** | REST + JSON                              | Estándar para la interacción entre el frontend y el backend. |
| **Frontend** | React, TypeScript, Vite, HTML5, CSS3     | Biblioteca JavaScript para UI, tipado fuerte, empaquetador rápido, y estándares web. |
| **Estilos** | Custom CSS, PostCSS, Tailwind CSS        | Estilos personalizados y utilitarios CSS para un diseño responsivo. |

-----

## 🗂️ Diagrama de la Estructura del Proyecto

-----

## 🚀 Inicio Rápido

Sigue estos pasos para levantar el proyecto en tu entorno local.

### 1\. Clonar el Repositorio

```bash
git clone https://github.com/tu_usuario/WeatherMaster.git
cd WeatherMaster
```

### 2\. Configuración del Backend (Python/FastAPI)

1.  **Instalar Dependencias de Python:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Configurar Variables de Entorno:**
    Copia el archivo de ejemplo y edítalo con tus claves.

    ```bash
    cp .env.example .env
    ```

    Abre `.env` y añade tu clave de API de OpenWeatherMap:

    ```
    WEATHER_API_KEY=tu_clave_api_openweathermap
    DATABASE_URL=sqlite:///./weather.db
    ```

3.  **Obtener tu Clave de API de OpenWeatherMap:**

      * Regístrate en [OpenWeatherMap](https://openweathermap.org/api).
      * Copia tu clave de API y pégala en el archivo `.env`.

4.  **Iniciar el Servidor Backend:**

    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

    El backend estará disponible en `http://localhost:8000`.

### 3\. Configuración del Frontend (React/TypeScript)

1.  **Instalar Dependencias de Node.js:**

    ```bash
    npm install
    ```

2.  **Iniciar el Servidor de Desarrollo Frontend:**

    ```bash
    npm run dev
    ```

    El frontend estará disponible en `http://localhost:5173` (o el puerto que Vite asigne).

### 4\. Abrir en tu Navegador

Una vez que ambos servidores (backend y frontend) estén ejecutándose:

  * Navega a la URL de tu frontend (ej. `http://localhost:5173`) para interactuar con la aplicación.
  * Puedes probar los endpoints de la API directamente en `http://localhost:8000/docs` (documentación interactiva de FastAPI).

-----

## 📊 Endpoints de la API

Los siguientes endpoints están disponibles a través de la API de FastAPI:

  * `GET /health`

      * **Descripción**: Verifica el estado y la disponibilidad de la API.
      * **Respuesta**: `{ "status": "ok" }`

  * `GET /weather/current/{city_name}`

      * **Descripción**: Obtiene las condiciones climáticas actuales para una ciudad específica.
      * **Parámetros**:
          * `city_name` (string, path): El nombre de la ciudad.
      * **Ejemplo**: `GET /weather/current/London`

  * `GET /weather/forecast/{city_name}`

      * **Descripción**: Obtiene el pronóstico del tiempo para los próximos 5 días para una ciudad específica.
      * **Parámetros**:
          * `city_name` (string, path): El nombre de la ciudad.
      * **Ejemplo**: `GET /weather/forecast/New%20York`

-----

## 🎨 Características del Frontend

La aplicación cuenta con una interfaz de usuario moderna y limpia, diseñada para ser intuitiva y visualmente atractiva:

  * **Diseño Responsivo**: Se adapta a pantallas de escritorio, tabletas y móviles.
  * **Iconos Climáticos Dinámicos**: Muestra iconos que cambian según las condiciones meteorológicas.
  * **Animaciones Suaves**: Incluye animaciones para iconos flotantes y transiciones de estado.
  * **Manejo de Errores**: Proporciona mensajes de error amigables al usuario.
  * **Estados de Carga**: Muestra indicadores visuales durante las llamadas a la API.

-----

## 🔧 Configuración Adicional

Puedes configurar los siguientes parámetros editando el archivo `.env`:

  * `WEATHER_API_KEY`: Tu clave personal de API de OpenWeatherMap.
  * `DATABASE_URL`: La URL de conexión a la base de datos SQLite (ej. `sqlite:///./weather.db`).

-----

## 🤝 Contribución

¡Las contribuciones son bienvenidas\! Si deseas mejorar el proyecto, sigue estos pasos:

1.  Haz un "fork" del repositorio.
2.  Crea una nueva rama para tu característica (`git checkout -b feature/nueva-caracteristica`).
3.  Realiza tus cambios y commitea (`git commit -am 'feat: añade nueva característica'`).
4.  Haz un "push" a la rama (`git push origin feature/nueva-caracteristica`).
5.  Abre un "Pull Request".

-----

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

-----

## 🌟 Soporte

Si encuentras útil este proyecto o te gusta, por favor, ¡dale una estrella en GitHub\! ⭐

-----