☁️ Aplicación del Clima con Open-Meteo
Una aplicación de consola en Python que consulta el clima actual y el pronóstico de 5 días para cualquier ciudad del mundo, usando la API gratuita de Open-Meteo.

🚀 Características

Clima actual: temperatura, humedad, viento, precipitación y descripción del estado del cielo
Pronóstico extendido para los próximos 5 días
Caché en memoria para evitar peticiones repetidas a la API
Manejo de errores de red y respuestas inválidas
Sin necesidad de API key


📦 Requisitos

Python 3.7 o superior
Librería requests


⚙️ Instalación

Clona o descarga este repositorio.
Instala la dependencia necesaria:

bashpip install requests

▶️ Uso
Ejecuta el archivo principal:
bashpython main.py
Cuando se te pida, ingresa el nombre de una ciudad:
Ingresa el nombre de una ciudad: Bogotá
Verás dos secciones en consola: el reporte del clima actual y el pronóstico de los próximos 5 días.

📁 Estructura del proyecto
├── main.py       # Archivo principal con toda la lógica
└── clima.py      # Módulo auxiliar importado por main.py

🌐 API utilizada
Los datos climáticos son provistos por Open-Meteo.

Sitio web: https://open-meteo.com
Licencia: CC BY 4.0
No requiere registro ni API key


📄 Licencia
Este proyecto hace uso de datos bajo licencia CC BY 4.0 provistos por Open-Meteo. Asegúrate de mantener la atribución correspondiente si distribuyes o modificás esta aplicación.