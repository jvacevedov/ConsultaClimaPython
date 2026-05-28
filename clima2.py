# ==========================================
# Aplicación simple de clima con Open-Meteo
# ==========================================
#
# ATRIBUCIÓN REQUERIDA (CC BY 4.0):
# Los datos climáticos son provistos por Open-Meteo
# Sitio web: https://open-meteo.com
# Licencia:  https://open-meteo.com/en/license
# ==========================================

# Librería necesaria:
# Instalar con:
# pip install requests

import requests

import clima

# ------------------------------------------
# Constantes
# ------------------------------------------

# URL de la API de geocodificación
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

# URL de la API del clima
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# Tiempo máximo de espera de la petición
TIMEOUT = 10

# Cache en memoria
cache_coordenadas = {}
cache_clima = {}
cache_pronostico = {}
# ------------------------------------------
# Función para traducir códigos del clima
# ------------------------------------------
def obtener_descripcion_clima(weather_code):
    """
    Convierte el código del clima en un texto entendible.
    """

    codigos_clima = {
        0: "Despejado",
        1: "Principalmente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        48: "Niebla con escarcha",
        51: "Llovizna ligera",
        53: "Llovizna moderada",
        55: "Llovizna intensa",
        61: "Lluvia ligera",
        63: "Lluvia moderada",
        65: "Lluvia fuerte",
        71: "Nieve ligera",
        73: "Nieve moderada",
        75: "Nieve intensa",
        80: "Chubascos ligeros",
        81: "Chubascos moderados",
        82: "Chubascos fuertes",
        95: "Tormenta"
    }

    return codigos_clima.get(weather_code, "Clima desconocido")

def obtener_icono_clima(codigo):
    iconos = {
        0: "☀️",
        1: "🌤️",
        2: "⛅",
        3: "☁️",
        45: "🌫️",
        61: "🌧️",
        71: "❄️",
        95: "⛈️"
    }

    return iconos.get(codigo, "🌍")
# ------------------------------------------
# Función para obtener coordenadas
# ------------------------------------------
def obtener_coordenadas(ciudad):
    """
    Busca la latitud y longitud de una ciudad.
    """

    # Verificar si ya está en cache
    if ciudad in cache_coordenadas:
        print("⚡ Datos obtenidos desde cache")
        return cache_coordenadas[ciudad]

    parametros = {
        "name": ciudad,
        "count": 1,
        "language": "es",
        "format": "json"
    }

    try:
        respuesta = requests.get(
            GEOCODING_URL,
            params=parametros,
            timeout=TIMEOUT
        )

        # Verifica si la respuesta fue correcta
        respuesta.raise_for_status()

        datos = respuesta.json()

        # Verifica si la ciudad existe
        if "results" not in datos:
            print("❌ Error: Ciudad no encontrada.")
            return None

        ciudad_info = datos["results"][0]

        resultado= {
            "nombre": ciudad_info["name"],
            "latitud": ciudad_info["latitude"],
            "longitud": ciudad_info["longitude"]
        }
    # Guardar en cache
        cache_coordenadas[ciudad] = resultado

        return resultado

    except requests.exceptions.Timeout:
        print("❌ Error: La solicitud tardó demasiado.")
        return None

    except requests.exceptions.ConnectionError:
        print("❌ Error: Problema de conexión a internet.")
        return None

    except requests.exceptions.RequestException as error:
        print(f"❌ Error en la API: {error}")
        return None


# ------------------------------------------
# Función para obtener el clima
# ------------------------------------------
def obtener_clima(latitud, longitud):
    """
    Consulta el clima actual usando coordenadas.
    """
    clave = f"{latitud},{longitud}"

    if clave in cache_clima:
        print("Usando clima desde cache...")
        return cache_clima[clave]

    parametros = {
            "latitude": latitud,
            "longitude": longitud,

             # Datos actuales
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "wind_speed_10m",
                "precipitation",
                "weather_code"
            ]
    }

    try:
        respuesta = requests.get(
            WEATHER_URL,
            params=parametros,
            timeout=TIMEOUT
        )

        # Verifica si la respuesta fue correcta
        respuesta.raise_for_status()

        datos = respuesta.json()

        # Verifica si existe información del clima
        if "current" not in datos:
            print("❌ Error: No se pudo obtener el clima.")
            return None

        clima_actual = datos["current"]

        resultado = {
            "temperatura": clima_actual["temperature_2m"],
            "codigo_clima": clima_actual["weather_code"],
            "viento": clima_actual["wind_speed_10m"],
            "precipitacion": clima_actual["precipitation"],
            "humedad": clima_actual["relative_humidity_2m"]
        }
        # Guardar en cache
        cache_clima[clave] = resultado

        return resultado

    except requests.exceptions.Timeout:
        print("❌ Error: La solicitud tardó demasiado.")
        return None

    except requests.exceptions.ConnectionError:
        print("❌ Error: Problema de conexión a internet.")
        return None

    except requests.exceptions.RequestException as error:
        print(f"❌ Error en la API: {error}")
        return None
# ------------------------------------------
# Función para obtener pronóstico de 5 días
# ------------------------------------------
def obtener_pronostico_5_dias(latitud, longitud):
    """
    Obtiene el pronóstico del clima para los próximos 5 días.
    """
    clave = f"{latitud},{longitud}"

    if clave in cache_pronostico:
        print("Usando pronóstico desde cache...")
        return cache_pronostico[clave]

    parametros = {
        "latitude": latitud,
        "longitude": longitud,

        # Datos diarios
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "wind_speed_10m_max"
        ],

        "timezone": "auto",
        "forecast_days": 5
    }

    try:
        respuesta = requests.get(
            WEATHER_URL,
            params=parametros,
            timeout=TIMEOUT
        )

        respuesta.raise_for_status()

        datos = respuesta.json()

        if "daily" not in datos:
            print("❌ Error: No se pudo obtener el pronóstico.")
            return None

        daily = datos["daily"]

        pronostico = []

        for i in range(len(daily["time"])):

            pronostico.append({
                "fecha": daily["time"][i],
                "temp_max": daily["temperature_2m_max"][i],
                "temp_min": daily["temperature_2m_min"][i],
                "precipitacion": daily["precipitation_sum"][i],
                "viento": daily["wind_speed_10m_max"][i],
                "codigo_clima": daily["weather_code"][i]
            })

        # Guardar en cache
        cache_pronostico[clave] = pronostico

        return pronostico

    except requests.exceptions.Timeout:
        print("❌ Error: La solicitud tardó demasiado.")
        return None

    except requests.exceptions.ConnectionError:
        print("❌ Error: Problema de conexión a internet.")
        return None

    except requests.exceptions.RequestException as error:
        print(f"❌ Error en la API: {error}")
        return None





# ------------------------------------------
# Función principal
# ------------------------------------------
def mostrar_reporte_clima(ciudad):
    """
    Muestra el reporte del clima en consola.
    """

    # Validar que la ciudad no esté vacía
    if not ciudad or ciudad.strip() == "":
        print("❌ Error: Debes ingresar una ciudad válida.")
        return

    # Obtener coordenadas
    coordenadas = obtener_coordenadas(ciudad)

    # Si ocurrió un error, detener el programa
    if coordenadas is None:
        return

    # Obtener clima actual
    clima = obtener_clima(
        coordenadas["latitud"],
        coordenadas["longitud"]
    )

    # Si ocurrió un error, detener el programa
    if clima is None:
        return

    # Obtener descripción del clima
    descripcion = obtener_descripcion_clima(clima["codigo_clima"])
    icono = obtener_icono_clima(clima["codigo_clima"])

    # Mostrar reporte en consola
    print("\n" + "=" * 45)
    print("        ☁️  REPORTE DEL CLIMA ☁️")
    print("=" * 45)

    print(f"📍 Ciudad:        {coordenadas['nombre']}")
    print(f"🌡️ Temperatura:  {clima['temperatura']} °C")
    print(f"💧 Humedad:      {clima['humedad']} %")
    print(f"🌬️ Viento:       {clima['viento']} km/h")
    print(f"🌧️ Precipitación:{clima['precipitacion']} mm")
    print(f"🌤️ Clima:        {icono} {descripcion}")
    print("=" * 45)
    print("📊 Datos: Open-Meteo.com | Licencia: CC BY 4.0")
    print("   https://open-meteo.com/en/license")
    print("=" * 45)

# ------------------------------------------
# Mostrar pronóstico extendido
# ------------------------------------------
def mostrar_pronostico_5_dias(ciudad):
    """
    Muestra el pronóstico del clima para 5 días.
    """

    coordenadas = obtener_coordenadas(ciudad)

    if coordenadas is None:
        return

    pronostico = obtener_pronostico_5_dias(
        coordenadas["latitud"],
        coordenadas["longitud"]
    )

    if pronostico is None:
        return

    print("\n" + "=" * 60)
    print(f"      📅 PRONÓSTICO 5 DÍAS - {coordenadas['nombre']}")
    print("=" * 60)

    for dia in pronostico:

        descripcion = obtener_descripcion_clima(
            dia["codigo_clima"]
        )

        icono = obtener_icono_clima(
            dia["codigo_clima"]
        )

        print(f"\n📆 Fecha: {dia['fecha']}")
        print(f"🌤️ Clima: {icono} {descripcion}")
        print(f"🌡️ Máx:   {dia['temp_max']} °C")
        print(f"🥶 Mín:   {dia['temp_min']} °C")
        print(f"🌧️ Lluvia:{dia['precipitacion']} mm")
        print(f"🌬️ Viento:{dia['viento']} km/h")
        print("=" * 60)
        print("📊 Datos: Open-Meteo.com | Licencia: CC BY 4.0")
        print("   https://open-meteo.com/en/license")
        print("=" * 60)

# ------------------------------------------
# Ejecución del programa
# ------------------------------------------

# Pedir ciudad al usuario
nombre_ciudad = input("Ingresa el nombre de una ciudad: ")

# Mostrar reporte
mostrar_reporte_clima(nombre_ciudad)
mostrar_pronostico_5_dias(nombre_ciudad)